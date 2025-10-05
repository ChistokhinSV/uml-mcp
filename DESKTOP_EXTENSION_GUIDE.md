# Claude Desktop Extension - Quick Start Guide

## ✅ What Was Created

Based on [Anthropic's Desktop Extensions](https://www.anthropic.com/engineering/desktop-extensions) documentation, the following files were created:

### Extension Files
```
extension/
├── manifest.json          # Extension configuration (MCP specification)
├── build.sh              # Build script for Linux/Mac
├── build.ps1             # Build script for Windows
├── README.md            # Extension documentation
├── ICON_PLACEHOLDER.md  # Icon creation guide
└── .gitignore           # Ignore build artifacts
```

### Updated Files
- `README.md` - Added Desktop Extension installation as **recommended method** (before manual config)
- `.gitignore` - Exclude `*.mcpb` build files

---

## 🚀 How to Use (For End Users)

### Step 1: Build the Extension Package

**On Linux/Mac:**
```bash
cd extension
./build.sh
```

**On Windows:**
```powershell
cd extension
.\build.ps1
```

This creates `uml-mcp.mcpb` in the project root.

### Step 2: Install in Claude Desktop

**Option A: Double-Click (Easiest)**
1. Double-click `uml-mcp.mcpb`
2. Claude Desktop opens and prompts for configuration
3. Enter output directory (default: `~/Documents/UML-MCP/diagrams`)
4. Click "Install"

**Option B: Manual Import**
1. Open Claude Desktop
2. Settings → Extensions
3. Click "Import Extension"
4. Select `uml-mcp.mcpb`
5. Configure and install

### Step 3: Start Using
1. Open Claude Desktop
2. Ask Claude to generate a diagram:
   ```
   "Create a UML class diagram showing User and Order entities with a one-to-many relationship"
   ```
3. Diagrams are automatically saved to your configured directory

---

## 📋 Extension Features

### User Configuration Options

The extension exposes these settings during installation:

1. **Output Directory** (Required)
   - Default: `~/Documents/UML-MCP/diagrams`
   - Where generated diagrams are saved

2. **Kroki Server URL** (Optional)
   - Default: `https://kroki.io`
   - Custom rendering server URL

3. **Use Local Kroki** (Optional)
   - Default: `false`
   - Enable for local Kroki instance

### Supported Tools (13 total)

- `generate_uml` - Universal diagram generator
- `generate_class_diagram` - UML class diagrams
- `generate_sequence_diagram` - UML sequence diagrams
- `generate_activity_diagram` - UML activity diagrams
- `generate_usecase_diagram` - UML use case diagrams
- `generate_state_diagram` - UML state diagrams
- `generate_component_diagram` - UML component diagrams
- `generate_deployment_diagram` - UML deployment diagrams
- `generate_object_diagram` - UML object diagrams
- `generate_mermaid_diagram` - Mermaid syntax
- `generate_d2_diagram` - D2 syntax
- `generate_graphviz_diagram` - Graphviz DOT syntax
- `generate_erd_diagram` - Entity-Relationship diagrams

### Supported Prompts (3 total)

- `class_diagram` - Create class diagrams
- `sequence_diagram` - Create sequence diagrams
- `activity_diagram` - Create activity diagrams

### Supported Resources

- `uml://types` - Available diagram types
- `uml://templates` - Diagram templates
- `uml://examples` - Example diagrams
- `uml://formats` - Output formats

---

## 🔧 Technical Details

### Extension Manifest (`manifest.json`)

The manifest follows the MCP Bundle (`.mcpb`) specification v1.0:

```json
{
  "mcpb_version": "1.0",
  "name": "uml-mcp",
  "version": "1.2.0",
  "display_name": "UML Diagram Generator",
  "server": {
    "type": "python",
    "command": "python",
    "args": ["${EXTENSION_DIR}/mcp_server.py"]
  },
  "dependencies": {
    "python": ">=3.10",
    "packages": [...]
  }
}
```

### Build Process

The build scripts create a `.mcpb` file (ZIP archive) containing:
```
uml-mcp.mcpb (ZIP)
├── manifest.json
├── icon.png (optional)
├── mcp_server.py
├── pyproject.toml
├── mcp_core/
├── kroki/
├── mermaid/
├── plantuml/
├── D2/
└── ai_uml/
```

### Platform Support

- ✅ **Windows** (win32) - Full support
- ✅ **macOS** (darwin) - Full support with uvloop
- ✅ **Linux** - Full support with uvloop

### Security

- API keys/secrets stored in OS keychain
- No embedded credentials
- Sandboxed per-user configuration

---

## 📦 Distribution Options

### Option 1: GitHub Releases (Recommended)

```bash
# Build the extension
./extension/build.sh

# Create GitHub release
gh release create v1.2.0 uml-mcp.mcpb \
  --title "UML-MCP Desktop Extension v1.2.0" \
  --notes "One-click installation for Claude Desktop"
```

Users can download from: `https://github.com/ChistokhinSV/uml-mcp/releases`

### Option 2: Direct Distribution

Share `uml-mcp.mcpb` via:
- Email
- Company intranet
- Cloud storage (Dropbox, Google Drive, etc.)

Users install by double-clicking or importing.

### Option 3: Anthropic Extension Directory (Future)

Submit to Anthropic for inclusion in Claude Desktop's extension directory:
1. Build and test the `.mcpb` package
2. Submit for review to Anthropic
3. Once approved, users find it in Claude Desktop → Extensions → Browse

---

## 🐛 Troubleshooting

### Extension Won't Install

**Issue:** "Failed to install extension"
- Ensure Python 3.10+ is installed
- Verify `.mcpb` file isn't corrupted (it's a ZIP - try unzipping manually)
- Check Claude Desktop logs

### Tools Not Appearing

**Issue:** Diagram tools don't show up in Claude
- Restart Claude Desktop
- Check Settings → Extensions → UML Diagram Generator is enabled
- Review extension logs

### Diagrams Not Generating

**Issue:** Tools run but diagrams don't appear
- Verify output directory exists and is writable
- Check Kroki server is accessible (default: https://kroki.io)
- Test network connectivity
- Check Claude Desktop logs for errors

### Checking Logs

**macOS:**
```bash
tail -f ~/Library/Logs/Claude/extension-uml-mcp.log
```

**Windows:**
```powershell
Get-Content $env:APPDATA\Claude\logs\extension-uml-mcp.log -Tail 20 -Wait
```

**Linux:**
```bash
tail -f ~/.config/Claude/logs/extension-uml-mcp.log
```

---

## 🎯 Next Steps

### For Development

1. **Add an icon:**
   - Create a 512x512 PNG icon
   - Place at `extension/icon.png`
   - Rebuild the extension

2. **Test the extension:**
   ```bash
   # Build
   ./extension/build.sh

   # Install in Claude Desktop (manual import)
   # Test all 13 tools
   # Verify configuration options work
   ```

3. **Publish to GitHub Releases:**
   ```bash
   gh release create v1.2.0 uml-mcp.mcpb
   ```

### For Users

1. **Download** `uml-mcp.mcpb` from releases
2. **Double-click** to install
3. **Configure** output directory
4. **Start using** - Ask Claude to generate diagrams!

---

## 📚 Resources

- [Desktop Extensions Blog Post](https://www.anthropic.com/engineering/desktop-extensions)
- [MCP Protocol Specification](https://modelcontextprotocol.io)
- [UML-MCP Repository](https://github.com/ChistokhinSV/uml-mcp)
- [Extension README](extension/README.md)

---

## ✨ Benefits Over Manual Configuration

| Feature | Desktop Extension | Manual Config |
|---------|------------------|---------------|
| Installation | One-click | Edit JSON files |
| Dependencies | Auto-managed | Manual install |
| Configuration UI | ✅ Yes | ❌ No |
| Updates | Automatic | Manual |
| Secret Storage | OS Keychain | Plain text |
| Cross-platform | ✅ Yes | Varies |
| Distribution | Single file | Multiple steps |

**Recommendation:** Use Desktop Extension for simplified, secure installation.

---

## 📄 License

Same as UML-MCP project - MIT License
