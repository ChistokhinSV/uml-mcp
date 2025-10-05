# Installation

This guide explains how to install and set up the UML-MCP server.

## System Requirements

- Python 3.10 or higher
- UV package manager (10-100x faster than pip)
- Optional: Docker for running local PlantUML or Kroki servers

## Installation Steps

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

## Verifying Installation

To verify your installation:

```bash
python mcp_server.py
```

You should see output similar to:

```
Starting UML-MCP Server v1.2.0
Server Name: UML Diagram Generator
Available Tools: 12
Available Prompts: 3
```

## IDE Integration

### Cursor

To integrate with Cursor IDE:

```bash
python mcp/install_to_cursor.py
```

This will automatically configure your Cursor IDE to use UML-MCP for diagram generation.

### Manual Configuration

For manual configuration in IDEs, you'll need to add UML-MCP as an MCP server with:

- Command: `python`
- Arguments: `["/path/to/uml-mcp/mcp_server.py"]`
- Output directory: `/path/to/store/diagrams`

## Optional Components

### Local Diagram Servers

For better performance or offline use, you can set up local servers:

#### PlantUML Server

```bash
docker run -d -p 8080:8080 plantuml/plantuml-server
```

#### Kroki Server

```bash
docker run -d -p 8000:8000 yuzutech/kroki
```

## Troubleshooting

If you encounter issues during installation:

1. Ensure Python 3.10+ is installed and in your PATH
2. Check that all required dependencies are installed
3. Verify any local servers are running correctly
4. Ensure proper permissions for the output directory
