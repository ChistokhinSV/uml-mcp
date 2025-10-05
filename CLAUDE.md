# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

UML-MCP is a diagram generation server implementing the Model Context Protocol (MCP). It provides seamless diagram creation through AI assistants, supporting multiple diagram types (UML, Mermaid, D2, Graphviz, etc.) with rendering via Kroki and PlantUML servers.

**Repository:** https://github.com/ChistokhinSV/uml-mcp

**Package Manager:** UV (required) - 10-100x faster than pip

## Development Commands

### Installation

**Prerequisites:** UV package manager must be installed first.

**Install UV:**
```bash
# Windows
winget install --id=astral-sh.uv -e

# Linux/Mac
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or via pip (slower)
pip install uv
```

**Install Dependencies:**
```bash
# Using Make (recommended)
make install         # Production dependencies
make install-dev     # Development dependencies

# Or directly with UV
uv pip install -e .          # Production
uv pip install -e ".[dev]"   # Development
```

**Why UV?**
- 10-100x faster than pip/poetry
- Better dependency resolution
- Works with existing Python tools
- Written in Rust by Astral (makers of ruff)

### Running the Server
```bash
# Start MCP server (default: stdio transport)
python mcp_server.py

# With debug logging
python mcp_server.py --debug

# List available tools
python mcp_server.py --list-tools

# HTTP transport
python mcp_server.py --transport http --host 127.0.0.1 --port 8000
```

### Testing
```bash
# Run all tests
make test
pytest

# Run specific test file
pytest tests/test_diagram_tools.py

# Run with coverage
make coverage
pytest --cov=mcp_core --cov=kroki --cov=mermaid --cov=D2 --cov-report=html
```

### Code Quality
```bash
# Run all linting checks
make lint
pre-commit run --all-files

# Clean temporary files
make clean
```

### Docker
```bash
# Build Docker images
make docker-build

# Run services
make docker-run

# Run tests in Docker
make docker-test

# Stop containers
make docker-stop
```

## Architecture

### Core Components

**MCP Server Core** (`mcp_core/core/server.py`)
- Singleton MCP server instance via `get_mcp_server()`
- Registers tools, resources, and prompts
- Supports stdio and HTTP transports via `start_server(transport, host, port)`

**Diagram Tools** (`mcp_core/tools/diagram_tools.py`)
- Tools decorated with `@mcp_tool` for automatic registration
- Main tool: `generate_uml(diagram_type, code, output_dir)` - universal diagram generator
- Specific tools per diagram type (e.g., `generate_class_diagram`, `generate_sequence_diagram`)
- All tools call `generate_diagram()` from `mcp_core/core/utils.py`

**Diagram Generation** (`mcp_core/core/utils.py`)
- `generate_diagram(diagram_type, code, output_format, output_dir)` - core generation logic
- Uses Kroki client (`kroki/kroki.py`) for rendering
- Automatically wraps PlantUML code with `@startuml/@enduml` if missing
- Returns dict with: `code`, `url`, `playground`, `local_path`, optionally `error`

**Configuration** (`mcp_core/core/config.py`)
- `MCP_SETTINGS` singleton with server configuration
- `DIAGRAM_TYPES` dict mapping diagram types to backends and descriptions
- Environment variable support for server URLs and output directory

**FastMCP Wrapper** (`mcp_core/server/fastmcp_wrapper.py`)
- Provides mock implementation for testing (auto-detects via `pytest` in sys.modules or env vars)
- Production mode uses real `fastmcp` package
- Mock mode creates lightweight stubs for development

### Supported Diagram Types

**UML (PlantUML backend):** class, sequence, activity, usecase, state, component, deployment, object

**Other:** mermaid, d2, graphviz, erd, blockdiag, bpmn, c4plantuml

### AI/ML Diagram Components

The `ai_uml/` package provides programmatic diagram generation for ML architectures:
- Block-based diagram building (encoders, decoders, attention, etc.)
- JSON-based diagram definitions
- SVG output via `svgwrite`
- Separate from MCP server functionality

## Environment Variables

```bash
# Server configuration
MCP_OUTPUT_DIR="/path/to/output"          # Default: ./output
KROKI_SERVER="https://kroki.io"           # Default: https://kroki.io
PLANTUML_SERVER="http://localhost:8080"   # Default: http://plantuml-server:8080
USE_LOCAL_KROKI="true"                    # Use local Kroki server
USE_LOCAL_PLANTUML="true"                 # Use local PlantUML server

# Development/Testing
LOG_LEVEL="DEBUG"                         # Logging level
TESTING="true"                            # Enable test mode
MOCK_FASTMCP="true"                       # Use mock FastMCP implementation
LIST_TOOLS="true"                         # Display tools and exit
```

## Cross-Platform Async Support

The server automatically detects the platform and uses the best event loop:
- **Linux/Mac**: Uses `uvloop` for improved async performance (auto-installed via `requirements.txt`)
- **Windows**: Uses default `asyncio` event loop (uvloop skipped automatically)

Platform detection uses pip environment markers: `uvloop>=0.17.0; sys_platform != "win32"`

This is handled automatically in both:
- `requirements.txt` - conditional installation
- `app.py` - runtime platform detection

No manual configuration needed.

## Editor Integration

### Claude Desktop
Add to `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "uml_diagram_generator": {
      "command": "python",
      "args": ["/path/to/uml-mcp/mcp_server.py"]
    }
  }
}
```

### Cursor
Add to Cursor MCP settings:
```json
{
  "mcpServers": {
    "uml_diagram_generator": {
      "command": "python",
      "args": ["/path/to/uml-mcp/mcp_server.py"]
    }
  }
}
```

## Important Patterns

### Adding New Diagram Tools
1. Define tool function with `@mcp_tool` decorator in `mcp_core/tools/diagram_tools.py`
2. Tool automatically registers via `register_diagram_tools()` called in `server.py`
3. Add diagram type configuration to `DIAGRAM_TYPES` in `mcp_core/core/config.py`

### Testing with Mock FastMCP
- Tests automatically use mock implementation (detected via `pytest` in `sys.modules`)
- Set `MOCK_FASTMCP=true` for manual mock mode
- Mock server in `fastmcp_wrapper.py` provides minimal MCP protocol implementation

### Diagram Code Processing
- PlantUML diagrams automatically wrapped with `@startuml/@enduml` markers
- Code validation happens in `generate_uml()` against `MCP_SETTINGS.diagram_types`
- All generation flows through single `generate_diagram()` function for consistency

## Local Development with Rendering Servers

```bash
# Start PlantUML server
docker run -d -p 8080:8080 plantuml/plantuml-server

# Start Kroki server
docker run -d -p 8000:8000 yuzutech/kroki

# Configure environment
export USE_LOCAL_PLANTUML=true
export PLANTUML_SERVER=http://localhost:8080
export USE_LOCAL_KROKI=true
export KROKI_SERVER=http://localhost:8000
```

## Logging

- Logs stored in `logs/uml_mcp_server_YYYY-MM-DD.log`
- Configured in `mcp_core/core/utils.py:setup_logging()`
- Both file and console handlers with timestamp, name, level, message format

## Code Review Guidelines

These guidelines are used by the AI code reviewer in GitHub Actions and should be followed for all code contributions.

### Python Code Standards

**Style & Formatting:**
- Follow PEP 8 conventions
- Line length: 88 characters (Black formatter)
- Use type hints for function parameters and return values
- Prefer f-strings over `.format()` or `%` formatting

**Documentation:**
- All public functions/classes must have docstrings
- Use Google-style docstrings with Args, Returns, Raises sections
- Complex logic should have inline comments explaining "why", not "what"

**Error Handling:**
- Use specific exception types, not bare `except:`
- Always log errors with context before raising/returning
- Validate user inputs and diagram code for injection attacks
- Handle file I/O errors gracefully (permissions, disk space, etc.)

### Architecture & Design

**MCP Protocol:**
- Use `@mcp_tool` decorator for all tools
- Tools must return dict with: `code`, `url`, `playground`, `local_path`
- Include error messages in return dict if generation fails
- Follow the single-responsibility principle for tool functions

**Async/Concurrency:**
- Use `async`/`await` for I/O operations
- Respect platform differences (uvloop on Linux/Mac, asyncio on Windows)
- Close resources properly (use context managers)

**Separation of Concerns:**
- Tools layer: `mcp_core/tools/` - MCP tool definitions only
- Core logic: `mcp_core/core/` - diagram generation, server setup
- Clients: `kroki/`, `mermaid/`, etc. - external service integrations
- Tests: `tests/` - comprehensive test coverage

### Security Best Practices

**Input Validation:**
- Sanitize all user-provided diagram code
- Validate diagram types against `DIAGRAM_TYPES` whitelist
- Check file paths to prevent directory traversal (no `../` in paths)
- Limit diagram code size to prevent DoS

**Path Safety:**
- Always use `os.path.join()` or `Path()` for file paths
- Validate output directories exist and are writable
- Never execute user-provided code directly
- Use subprocess with shell=False when calling external tools

**Secrets Management:**
- Never hardcode API keys or tokens
- Use environment variables for configuration
- Don't log sensitive information (API keys, file contents)
- Exclude `.env` files from version control

### Testing Requirements

**Test Coverage:**
- Minimum 70% code coverage (ideally 80%+)
- Unit tests for all new functions
- Integration tests for diagram generation workflows
- Test both success and failure paths

**Test Quality:**
- Use pytest fixtures for common setup
- Mock external dependencies (Kroki, PlantUML servers)
- Test cross-platform compatibility (Windows vs Linux)
- Include edge cases and error conditions

**Test Organization:**
- One test file per module: `test_<module_name>.py`
- Descriptive test names: `test_<function>_<scenario>_<expected>`
- Group related tests in classes: `class TestDiagramTools:`

### Performance Considerations

**Optimization:**
- Cache diagram results when possible
- Use streaming for large file operations
- Minimize API calls to external services
- Profile code for performance bottlenecks

**Resource Management:**
- Close file handles after use
- Limit concurrent diagram generations
- Clean up temporary files
- Monitor memory usage for large diagrams

### Dependencies & Compatibility

**Package Management:**
- All dependencies in `pyproject.toml`
- Use version constraints: `"package>=1.0.0,<2.0.0"`
- Platform-specific deps: `"uvloop>=0.17.0; sys_platform != 'win32'"`
- Keep dependencies minimal and up-to-date

**Cross-Platform:**
- Test on Windows, macOS, and Linux
- Use `os.path` or `pathlib.Path` for paths
- Handle platform-specific event loops correctly
- Avoid platform-specific shell commands

**Python Versions:**
- Support Python 3.10+
- Use `requires-python = ">=3.10"` in pyproject.toml
- Avoid features from Python 3.11+ unless necessary
- Test on multiple Python versions in CI

### Documentation Standards

**README Updates:**
- Document new features and configuration options
- Update installation instructions if needed
- Add examples for new diagram types
- Keep compatibility matrix current

**CLAUDE.md Maintenance:**
- Update development commands for new workflows
- Document new architectural patterns
- Add troubleshooting for common issues
- Update important patterns section

**Code Comments:**
- Explain complex algorithms and business logic
- Document workarounds and known limitations
- Reference issue numbers for bug fixes
- Avoid obvious comments ("increment i by 1")

### Git & Pull Requests

**Commit Messages:**
- Use imperative mood: "Add feature" not "Added feature"
- First line: concise summary (50 chars max)
- Body: detailed explanation if needed
- Reference issues: "Fixes #123", "Relates to #456"

**PR Best Practices:**
- One feature/fix per PR
- Include tests for new functionality
- Update documentation in the same PR
- Keep PRs small and focused (< 400 lines changed)
