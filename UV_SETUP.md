# UV Package Manager - Quick Reference

UV is a fast Python package manager written in Rust, **10-100x faster** than pip and poetry.

This project uses UV exclusively for dependency management.

## Installation

### Windows (Recommended)
```powershell
winget install --id=astral-sh.uv -e
```

### Linux/Mac (Recommended)
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Alternative (Using pip - slower)
```bash
pip install uv
```

## Quick Start

```bash
# Clone the repository
git clone https://github.com/ChistokhinSV/uml-mcp.git
cd uml-mcp

# Install dependencies (production)
uv pip install -e .

# Install with development dependencies
uv pip install -e ".[dev]"
```

## Common Commands

### Install Dependencies
```bash
# Production dependencies
uv pip install -e .

# Development dependencies
uv pip install -e ".[dev]"
```

### Create Virtual Environment
```bash
# Create a virtual environment
uv venv

# Activate it
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate
```

### Run Commands
```bash
# Run commands directly in the venv
uv run python mcp_server.py
uv run pytest
```

### Manage Dependencies
```bash
# Add a new dependency
uv pip install <package-name>

# Update dependencies
uv pip install --upgrade <package-name>

# List installed packages
uv pip list
```

## Benefits of UV

1. **🚀 Speed**: 10-100x faster than pip/poetry
2. **🔧 Better dependency resolution**: Faster conflict detection
3. **🔄 Compatible**: Works with existing pyproject.toml
4. **💾 Built-in caching**: Shared cache across projects
5. **🦀 Rust-powered**: Built by Astral (makers of ruff)

## Makefile Integration

This project's Makefile uses UV:

```bash
make install        # Install production dependencies
make install-dev    # Install development dependencies
make test           # Run tests
make lint           # Run linting
```

## Migration Notes

This project has **migrated from pip to UV**:
- ❌ No more `requirements.txt` files
- ✅ All dependencies in `pyproject.toml`
- ✅ Faster installs (10-100x)
- ✅ Better dependency resolution

## Resources

- [UV Documentation](https://github.com/astral-sh/uv)
- [UV Installation Guide](https://astral.sh/uv/)
- [Project Repository](https://github.com/ChistokhinSV/uml-mcp)
