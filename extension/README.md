# Claude Desktop Extension for UML-MCP

This directory contains the Claude Desktop Extension package for UML-MCP, making it easy to install the diagram generation server with just a click.

## What is a Desktop Extension?

Claude Desktop Extensions (`.mcpb` files) are pre-packaged MCP servers that simplify installation by:
- Bundling the entire server into a single file
- Managing dependencies automatically
- Providing a simple configuration UI
- Storing secrets securely in the OS keychain
- Enabling one-click installation

## Structure

```
extension/
├── manifest.json          # Extension configuration
├── icon.png              # Extension icon (512x512)
├── README.md            # This file
└── build.sh             # Build script to create .mcpb package
```

## Building the Extension

### Prerequisites
- Python 3.10+
- UV package manager
- zip utility

### Build Steps

```bash
# From the project root directory
cd extension
./build.sh

# Or manually:
cd ..
zip -r uml-mcp.mcpb \
  extension/manifest.json \
  extension/icon.png \
  mcp_server.py \
  mcp_core/ \
  kroki/ \
  mermaid/ \
  plantuml/ \
  D2/ \
  pyproject.toml
```

This creates `uml-mcp.mcpb` which can be distributed and installed in Claude Desktop.

## Installation (For Users)

### Method 1: One-Click Install (Recommended)
1. Download `uml-mcp.mcpb`
2. Double-click the file
3. Claude Desktop will prompt for configuration
4. Enter your preferred output directory
5. Click "Install"

### Method 2: Manual Import
1. Open Claude Desktop
2. Go to Settings → Extensions
3. Click "Import Extension"
4. Select `uml-mcp.mcpb`
5. Configure settings and click "Install"

## Configuration

The extension exposes these user-configurable settings:

### Output Directory
- **Default:** `~/Documents/UML-MCP/diagrams`
- **Description:** Where generated diagrams are saved
- **Required:** Yes

### Kroki Server URL
- **Default:** `https://kroki.io`
- **Description:** Diagram rendering service URL
- **Required:** No

### Use Local Kroki Server
- **Default:** `false`
- **Description:** Enable if running a local Kroki instance
- **Required:** No

## Supported Platforms

- ✅ macOS (darwin)
- ✅ Linux
- ✅ Windows (win32)

## Distribution

### Publishing to Anthropic Extension Directory

To make this extension available in Claude Desktop's extension directory:

1. Build the `.mcpb` package
2. Submit to Anthropic for review
3. Once approved, users can install directly from Claude Desktop

### Self-Distribution

You can distribute the `.mcpb` file directly:
- Host on GitHub Releases
- Share via company intranet
- Email to team members

Users can install from any source using the manual import method.

## Security

- All secrets (API keys, tokens) are stored in the OS keychain
- No credentials are embedded in the extension
- Configuration is per-user and sandboxed

## Updates

Desktop Extensions support automatic updates:
- Users will be notified when a new version is available
- Updates can be installed with one click
- Rollback to previous versions is supported

## Troubleshooting

### Extension Won't Install
- Ensure Python 3.10+ is available on the system
- Check that all dependencies in `manifest.json` are valid
- Verify the `.mcpb` file isn't corrupted (should be a valid ZIP)

### Tools Not Appearing
- Restart Claude Desktop after installation
- Check extension is enabled in Settings → Extensions
- Review logs in Claude Desktop developer console

### Diagrams Not Generating
- Verify output directory exists and is writable
- Check Kroki server is accessible (if using custom URL)
- Ensure network connectivity for diagram rendering

## Development

To test changes during development:

```bash
# Build the extension
./build.sh

# Install in Claude Desktop
# (Use manual import method)

# Check logs
# macOS: ~/Library/Logs/Claude/
# Windows: %APPDATA%\Claude\logs\
# Linux: ~/.config/Claude/logs/
```

## Resources

- [Desktop Extensions Documentation](https://www.anthropic.com/engineering/desktop-extensions)
- [MCP Protocol Specification](https://modelcontextprotocol.io)
- [UML-MCP Repository](https://github.com/ChistokhinSV/uml-mcp)

## License

MIT License - Same as the main UML-MCP project
