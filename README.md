# UML-MCP: A Diagram Generation Server with MCP Interface

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![smithery badge](https://smithery.ai/badge/@antoinebou12/uml)](https://smithery.ai/server/@antoinebou12/uml)

UML-MCP is a powerful diagram generation server that implements the Model Context Protocol (MCP), enabling seamless diagram creation directly from AI assistants and other applications. 

## 🌟 Features

- **Claude Desktop Extension**: One-click installation via `.mcpb` package
- **Multiple Diagram Types**: Support for UML diagrams (Class, Sequence, Activity, etc.), Mermaid, D2, and more
- **MCP Integration**: Seamless integration with LLM assistants supporting the Model Context Protocol
- **Playground Links**: Direct links to online editors for each diagram type
- **Multiple Output Formats**: SVG, PNG, PDF, and other format options
- **Easy Configuration**: Works with local and remote diagram rendering services
- **Cross-Platform**: Works on Windows, macOS, and Linux

## 📋 Supported Diagram Types

UML-MCP supports a wide variety of diagram types:

| Category | Diagram Types |
|----------|---------------|
| UML | Class, Sequence, Activity, Use Case, State, Component, Deployment, Object |
| Other | Mermaid, D2, Graphviz, ERD, BlockDiag, BPMN, C4 with PlantUML |

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- UV package manager (10-100x faster than pip)

### Installation

1. Install UV package manager:

**Windows:**
```powershell
winget install --id=astral-sh.uv -e
```

**Linux/Mac:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Clone the repository:

```bash
git clone https://github.com/ChistokhinSV/uml-mcp.git
cd uml-mcp
```

3. Install the dependencies:

```bash
uv pip install -e .
```

4. For development environment:

```bash
uv pip install -e ".[dev]"
```

### Running the Server

Start the MCP server:

```bash
python mcp_server.py
```

This will start the server using stdio for communication with MCP clients.

## 🔧 Configuration

### Claude Desktop Extension (Recommended)

The easiest way to install UML-MCP is using the Claude Desktop Extension:

#### One-Click Installation

1. **Download the extension:**
   ```bash
   # Build the extension package
   cd extension
   ./build.sh           # Linux/Mac
   # or
   .\build.ps1          # Windows
   ```

2. **Install in Claude Desktop:**
   - Double-click `uml-mcp.mcpb`
   - Or: Claude Desktop → Settings → Extensions → Import Extension
   - Configure output directory and click "Install"

3. **Start using:**
   - Open Claude Desktop
   - Ask Claude to generate diagrams
   - Diagrams are automatically saved to your configured directory

**Benefits:**
- ✅ One-click installation
- ✅ Automatic dependency management
- ✅ Secure configuration storage
- ✅ Cross-platform support
- ✅ Automatic updates

---

### Editor Integration

#### Claude Desktop (Manual Configuration)

If you prefer manual configuration or the extension isn't available:

**On MacOS:** `~/Library/Application\ Support/Claude/claude_desktop_config.json`
**On Windows:** `%APPDATA%/Claude/claude_desktop_config.json`

<details>
  <summary>Claude Desktop Manual Configuration</summary>

  ```json
  {
    "mcpServers": {
      "uml_diagram_generator": {
        "command": "python",
        "args": [
          "/path/to/uml-mcp/mcp_server.py"
        ],
        "env": {
          "MCP_OUTPUT_DIR": "/path/to/output/directory"
        }
      }
    }
  }
  ```
</details>

#### Cursor

To integrate with Cursor:

<details>
  <summary>Cursor Configuration</summary>

```json
{
  "mcpServers": {
    "UML-MCP-Server": {
      "command": "python",
      "args": ["/path/to/uml-mcp/mcp_server.py"],
      "env": {
        "MCP_OUTPUT_DIR": "/path/to/output"
      }
    }
  }
}
```
</details>

### Environment Variables

- `MCP_OUTPUT_DIR` - Directory to save generated diagrams (default: `./output`)
- `KROKI_SERVER` - URL of the Kroki server (default: `https://kroki.io`)
- `PLANTUML_SERVER` - URL of the PlantUML server (default: `http://plantuml-server:8080`)
- `USE_LOCAL_KROKI` - Use local Kroki server (true/false)
- `USE_LOCAL_PLANTUML` - Use local PlantUML server (true/false)

## 📚 Documentation

For detailed documentation, visit the [docs](./docs) directory or our [documentation site](https://uml-mcp.readthedocs.io/).

## 🧩 Architecture

UML-MCP is built with a modular architecture:

- **MCP Server Core**: Handles MCP protocol communication
- **Diagram Generators**: Supporting different diagram types
- **Tools**: Expose diagram generation functionality through MCP
- **Resources**: Provide templates and examples for various diagram types

## 🛠️ Local Development

For local development:

1. Set up local PlantUML and/or Kroki servers:

```bash
# PlantUML
docker run -d -p 8080:8080 plantuml/plantuml-server

# Kroki
docker run -d -p 8000:8000 yuzutech/kroki
```

2. Configure environment variables:

```bash
export USE_LOCAL_PLANTUML=true
export PLANTUML_SERVER=http://localhost:8080
export USE_LOCAL_KROKI=true  
export KROKI_SERVER=http://localhost:8000
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👏 Acknowledgements

- [PlantUML](https://plantuml.com/) - UML diagram generation
- [Kroki](https://kroki.io/) - Unified diagram generation service
- [Mermaid](https://mermaid.js.org/) - Generation of diagrams from text
- [D2](https://d2lang.com/) - Modern diagram scripting language

# UML-MCP Server

An MCP Server that provides UML diagram generation capabilities through various diagram rendering engines.

## Components

### Resources

The server provides several resources via the `uml://` URI scheme:

- `uml://types`: List of available UML diagram types
- `uml://templates`: Templates for creating UML diagrams
- `uml://examples`: Example UML diagrams for reference
- `uml://formats`: Supported output formats for diagrams
- `uml://server-info`: Information about the UML-MCP server

### Tools

The server implements multiple diagram generation tools:

#### Universal UML Generator
- `generate_uml`: Generate any UML diagram
  - Parameters: `diagram_type`, `code`, `output_dir`

#### Specific UML Diagram Tools
- `generate_class_diagram`: Generate UML class diagrams
  - Parameters: `code`, `output_dir`
- `generate_sequence_diagram`: Generate UML sequence diagrams
  - Parameters: `code`, `output_dir`
- `generate_activity_diagram`: Generate UML activity diagrams
  - Parameters: `code`, `output_dir`
- `generate_usecase_diagram`: Generate UML use case diagrams
  - Parameters: `code`, `output_dir`
- `generate_state_diagram`: Generate UML state diagrams
  - Parameters: `code`, `output_dir`
- `generate_component_diagram`: Generate UML component diagrams
  - Parameters: `code`, `output_dir`
- `generate_deployment_diagram`: Generate UML deployment diagrams
  - Parameters: `code`, `output_dir`
- `generate_object_diagram`: Generate UML object diagrams
  - Parameters: `code`, `output_dir`

#### Other Diagram Formats
- `generate_mermaid_diagram`: Generate diagrams using Mermaid syntax
  - Parameters: `code`, `output_dir`
- `generate_d2_diagram`: Generate diagrams using D2 syntax
  - Parameters: `code`, `output_dir`
- `generate_graphviz_diagram`: Generate diagrams using Graphviz DOT syntax
  - Parameters: `code`, `output_dir`
- `generate_erd_diagram`: Generate Entity-Relationship diagrams
  - Parameters: `code`, `output_dir`

### Prompts

The server provides prompts to help create UML diagrams:

- `class_diagram`: Create a UML class diagram showing classes, attributes, methods, and relationships
- `sequence_diagram`: Create a UML sequence diagram showing interactions between objects over time
- `activity_diagram`: Create a UML activity diagram showing workflows and business processes

## Advanced Configuration

See the [Configuration](#-configuration) section above for Claude Desktop Extension installation or manual setup options.

## Usage

### Command Line Arguments

```
usage: mcp_server.py [-h] [--debug] [--host HOST] [--port PORT] [--transport {stdio,http}] [--list-tools]

UML-MCP Diagram Generation Server

options:
  -h, --help            show this help message and exit
  --debug               Enable debug logging
  --host HOST           Server host (default: 127.0.0.1)
  --port PORT           Server port (default: 8000)
  --transport {stdio,http}
                        Transport protocol (default: stdio)
  --list-tools          List available tools and exit
```

### Environment Variables

- `LOG_LEVEL`: Set logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `UML_MCP_OUTPUT_DIR`: Directory to store generated diagram files
- `KROKI_SERVER`: Kroki server URL for diagram rendering
- `PLANTUML_SERVER`: PlantUML server URL for diagram rendering
- `LIST_TOOLS`: Set to "true" to display tools and exit

### Example: Generating a Class Diagram

```python
result = tool.call("generate_class_diagram", {
    "code": """
        @startuml
        class User {
          -id: int
          -name: string
          +login(): boolean
        }
        class Order {
          -id: int
          +addItem(item: string): void
        }
        User "1" -- "many" Order
        @enduml
    """,
    "output_dir": "/path/to/output"
})
```

## Development

### Building and Running

```bash
# Clone the repository
git clone https://github.com/ChistokhinSV/uml-mcp.git
cd uml-mcp

# Install dependencies
uv pip install -e .

# Run the server
python mcp_server.py
```

### Debugging

For debugging, you can run the server with:

```bash
python mcp_server.py --debug
```

Debug logs will be stored in the `logs/` directory.

### Running Tests

```bash
# Run all tests
pytest

# Run specific tests
pytest tests/test_diagram_tools.py
```

