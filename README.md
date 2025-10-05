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

If you prefer manual configuration or the extension isn't available, you can manually configure the MCP server.

<details>
  <summary><b>📝 Step-by-Step Manual Installation</b></summary>

  ### 1. Install Dependencies

  First, ensure UV and project dependencies are installed:

  ```bash
  # Install UV package manager
  # Windows
  winget install --id=astral-sh.uv -e
  # Linux/Mac
  curl -LsSf https://astral.sh/uv/install.sh | sh

  # Clone and install UML-MCP
  git clone https://github.com/ChistokhinSV/uml-mcp.git
  cd uml-mcp
  uv pip install -e .
  ```

  ### 2. Locate Configuration File

  **macOS:**
  ```bash
  ~/Library/Application Support/Claude/claude_desktop_config.json
  ```

  **Windows:**
  ```
  %APPDATA%\Claude\claude_desktop_config.json
  ```
  (Typically: `C:\Users\YOUR_USERNAME\AppData\Roaming\Claude\claude_desktop_config.json`)

  **Linux:**
  ```bash
  ~/.config/Claude/claude_desktop_config.json
  ```

  ### 3. Edit Configuration File

  Create or edit the file with your preferred text editor:

  **macOS/Linux:**
  ```bash
  nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
  ```

  **Windows:**
  ```powershell
  notepad %APPDATA%\Claude\claude_desktop_config.json
  ```

  ### 4. Add UML-MCP Server Configuration

  <details>
    <summary><b>Basic Configuration</b></summary>

  ```json
  {
    "mcpServers": {
      "uml-mcp": {
        "command": "python",
        "args": [
          "/absolute/path/to/uml-mcp/mcp_server.py"
        ],
        "env": {
          "MCP_OUTPUT_DIR": "/path/to/output/directory"
        }
      }
    }
  }
  ```

  **Replace:**
  - `/absolute/path/to/uml-mcp/mcp_server.py` with your actual installation path
  - `/path/to/output/directory` with where you want diagrams saved

  **Example (macOS):**
  ```json
  {
    "mcpServers": {
      "uml-mcp": {
        "command": "python3",
        "args": [
          "/Users/username/projects/uml-mcp/mcp_server.py"
        ],
        "env": {
          "MCP_OUTPUT_DIR": "/Users/username/Documents/UML-Diagrams"
        }
      }
    }
  }
  ```

  **Example (Windows):**
  ```json
  {
    "mcpServers": {
      "uml-mcp": {
        "command": "python",
        "args": [
          "C:\\Users\\username\\projects\\uml-mcp\\mcp_server.py"
        ],
        "env": {
          "MCP_OUTPUT_DIR": "C:\\Users\\username\\Documents\\UML-Diagrams"
        }
      }
    }
  }
  ```

  **Example (Linux):**
  ```json
  {
    "mcpServers": {
      "uml-mcp": {
        "command": "python3",
        "args": [
          "/home/username/projects/uml-mcp/mcp_server.py"
        ],
        "env": {
          "MCP_OUTPUT_DIR": "/home/username/Documents/UML-Diagrams"
        }
      }
    }
  }
  ```

  </details>

  <details>
    <summary><b>Advanced Configuration (with Custom Kroki Server)</b></summary>

  ```json
  {
    "mcpServers": {
      "uml-mcp": {
        "command": "python",
        "args": [
          "/absolute/path/to/uml-mcp/mcp_server.py"
        ],
        "env": {
          "MCP_OUTPUT_DIR": "/path/to/output/directory",
          "KROKI_SERVER": "https://kroki.io",
          "USE_LOCAL_KROKI": "false",
          "PLANTUML_SERVER": "http://localhost:8080",
          "USE_LOCAL_PLANTUML": "false"
        }
      }
    }
  }
  ```

  **Custom Kroki Server Example:**
  ```json
  {
    "mcpServers": {
      "uml-mcp": {
        "command": "python",
        "args": [
          "/Users/username/projects/uml-mcp/mcp_server.py"
        ],
        "env": {
          "MCP_OUTPUT_DIR": "/Users/username/Documents/UML-Diagrams",
          "KROKI_SERVER": "http://localhost:8000",
          "USE_LOCAL_KROKI": "true"
        }
      }
    }
  }
  ```

  </details>

  <details>
    <summary><b>Using Virtual Environment (Recommended)</b></summary>

  If you're using a Python virtual environment:

  ```json
  {
    "mcpServers": {
      "uml-mcp": {
        "command": "/absolute/path/to/uml-mcp/.venv/bin/python",
        "args": [
          "/absolute/path/to/uml-mcp/mcp_server.py"
        ],
        "env": {
          "MCP_OUTPUT_DIR": "/path/to/output/directory"
        }
      }
    }
  }
  ```

  **macOS/Linux Example:**
  ```json
  {
    "mcpServers": {
      "uml-mcp": {
        "command": "/Users/username/projects/uml-mcp/.venv/bin/python",
        "args": [
          "/Users/username/projects/uml-mcp/mcp_server.py"
        ],
        "env": {
          "MCP_OUTPUT_DIR": "/Users/username/Documents/UML-Diagrams"
        }
      }
    }
  }
  ```

  **Windows Example:**
  ```json
  {
    "mcpServers": {
      "uml-mcp": {
        "command": "C:\\Users\\username\\projects\\uml-mcp\\.venv\\Scripts\\python.exe",
        "args": [
          "C:\\Users\\username\\projects\\uml-mcp\\mcp_server.py"
        ],
        "env": {
          "MCP_OUTPUT_DIR": "C:\\Users\\username\\Documents\\UML-Diagrams"
        }
      }
    }
  }
  ```

  </details>

  ### 5. Restart Claude Desktop

  After saving the configuration file:
  1. Quit Claude Desktop completely
  2. Relaunch Claude Desktop
  3. The UML-MCP server should now be available

  ### 6. Verify Installation

  In Claude Desktop, try asking:
  ```
  "Generate a simple UML class diagram with User and Order classes"
  ```

  If successful, you'll see the diagram generated and saved to your output directory.

</details>

<details>
  <summary><b>🔧 Configuration Options Reference</b></summary>

  ### Required Fields

  | Field | Description | Example |
  |-------|-------------|---------|
  | `command` | Python executable path | `"python"` or `"python3"` |
  | `args` | Array with server script path | `["/path/to/mcp_server.py"]` |

  ### Environment Variables

  | Variable | Default | Description |
  |----------|---------|-------------|
  | `MCP_OUTPUT_DIR` | `./output` | Directory to save generated diagrams |
  | `KROKI_SERVER` | `https://kroki.io` | Kroki server URL for rendering |
  | `PLANTUML_SERVER` | `http://plantuml-server:8080` | PlantUML server URL |
  | `USE_LOCAL_KROKI` | `false` | Use local Kroki instance |
  | `USE_LOCAL_PLANTUML` | `false` | Use local PlantUML instance |
  | `LOG_LEVEL` | `INFO` | Logging level (DEBUG, INFO, WARNING, ERROR) |

  ### Example: Minimal Configuration

  ```json
  {
    "mcpServers": {
      "uml-mcp": {
        "command": "python",
        "args": ["/path/to/uml-mcp/mcp_server.py"]
      }
    }
  }
  ```

  **Note:** Without `MCP_OUTPUT_DIR`, diagrams save to `./output` in the server directory.

</details>

<details>
  <summary><b>⚠️ Troubleshooting</b></summary>

  ### Server Not Starting

  **Issue:** UML-MCP doesn't appear in Claude Desktop

  **Solutions:**
  1. Verify Python is in PATH: `python --version` or `python3 --version`
  2. Check file paths are absolute (not relative)
  3. Ensure `mcp_server.py` exists at specified path
  4. Review Claude Desktop logs:
     - **macOS:** `~/Library/Logs/Claude/mcp-server-uml-mcp.log`
     - **Windows:** `%APPDATA%\Claude\logs\mcp-server-uml-mcp.log`

  ### Import Errors

  **Issue:** `ModuleNotFoundError` or `ImportError`

  **Solutions:**
  1. Ensure dependencies are installed: `uv pip install -e .`
  2. Use virtual environment Python path in `command`
  3. Check UV installed packages: `uv pip list`

  ### Diagrams Not Generating

  **Issue:** Tools work but no diagram files appear

  **Solutions:**
  1. Verify `MCP_OUTPUT_DIR` exists and is writable
  2. Check directory permissions
  3. Try absolute path for output directory
  4. Test Kroki server connectivity: `curl https://kroki.io`

  ### Windows Path Issues

  **Issue:** Backslashes in paths causing errors

  **Solutions:**
  - Use double backslashes: `C:\\Users\\name\\path`
  - Or use forward slashes: `C:/Users/name/path`

  ### Permission Denied

  **Issue:** Cannot write to output directory

  **Solutions:**
  ```bash
  # macOS/Linux
  chmod 755 /path/to/output/directory

  # Windows (PowerShell as Admin)
  icacls "C:\path\to\output" /grant Users:F
  ```

</details>

#### Cursor

<details>
  <summary><b>📝 Cursor IDE Configuration</b></summary>

  ### 1. Locate Cursor Settings

  Cursor settings are typically located at:

  **macOS/Linux:**
  ```bash
  ~/.cursor/mcp_settings.json
  ```

  **Windows:**
  ```
  %APPDATA%\Cursor\User\mcp_settings.json
  ```

  ### 2. Configure MCP Server

  <details>
    <summary><b>Basic Configuration</b></summary>

  ```json
  {
    "mcpServers": {
      "uml-mcp": {
        "command": "python",
        "args": [
          "/absolute/path/to/uml-mcp/mcp_server.py"
        ],
        "env": {
          "MCP_OUTPUT_DIR": "/path/to/output/directory"
        }
      }
    }
  }
  ```

  **macOS Example:**
  ```json
  {
    "mcpServers": {
      "uml-mcp": {
        "command": "python3",
        "args": [
          "/Users/username/projects/uml-mcp/mcp_server.py"
        ],
        "env": {
          "MCP_OUTPUT_DIR": "/Users/username/Documents/UML-Diagrams"
        }
      }
    }
  }
  ```

  **Windows Example:**
  ```json
  {
    "mcpServers": {
      "uml-mcp": {
        "command": "python",
        "args": [
          "C:\\Users\\username\\projects\\uml-mcp\\mcp_server.py"
        ],
        "env": {
          "MCP_OUTPUT_DIR": "C:\\Users\\username\\Documents\\UML-Diagrams"
        }
      }
    }
  }
  ```

  </details>

  <details>
    <summary><b>Advanced Configuration</b></summary>

  ```json
  {
    "mcpServers": {
      "uml-mcp": {
        "command": "/path/to/.venv/bin/python",
        "args": [
          "/absolute/path/to/uml-mcp/mcp_server.py"
        ],
        "env": {
          "MCP_OUTPUT_DIR": "/path/to/output/directory",
          "KROKI_SERVER": "https://kroki.io",
          "USE_LOCAL_KROKI": "false",
          "LOG_LEVEL": "INFO"
        }
      }
    }
  }
  ```

  </details>

  ### 3. Restart Cursor

  After saving the configuration:
  1. Close all Cursor windows
  2. Restart Cursor
  3. UML-MCP tools should now be available

  ### 4. Verify Installation

  In Cursor, try using the MCP tools through the command palette or by asking the AI assistant to generate a diagram.

</details>

<details>
  <summary><b>🔧 Other MCP Clients</b></summary>

  UML-MCP works with any MCP-compatible client. General configuration format:

  ```json
  {
    "mcpServers": {
      "uml-mcp": {
        "command": "python",
        "args": ["/path/to/uml-mcp/mcp_server.py"],
        "env": {
          "MCP_OUTPUT_DIR": "/output/directory"
        }
      }
    }
  }
  ```

  Consult your MCP client's documentation for specific configuration file locations and formats.

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

