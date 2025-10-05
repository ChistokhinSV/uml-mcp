# Release Instructions for Maintainers

This guide explains how to create a new release of UML-MCP with the Desktop Extension.

## Prerequisites

- Write access to the repository
- Python 3.10+
- UV package manager installed
- GitHub CLI (`gh`) installed (optional, for CLI-based releases)

## Release Checklist

### 1. Update Version Numbers

Update version in the following files:
- `pyproject.toml` - `version` field
- `extension/manifest.json` - `version` field

Example:
```toml
# pyproject.toml
[project]
version = "1.3.0"
```

```json
// extension/manifest.json
{
  "version": "1.3.0"
}
```

### 2. Build the Extension Package

**Cross-platform method (recommended):**
```bash
cd extension
python build.py
```

This creates `uml-mcp.mcpb` in the project root (approximately 5-6 MB).

**Verify the build:**
- Check that `uml-mcp.mcpb` exists
- Check file size (should be 5-6 MB)
- Optionally: Test installation in Claude Desktop

### 3. Commit and Tag

```bash
git add pyproject.toml extension/manifest.json
git commit -m "Bump version to v1.3.0"
git tag v1.3.0
git push origin main
git push origin v1.3.0
```

### 4. Create GitHub Release

#### Option A: Using GitHub CLI

```bash
gh release create v1.3.0 uml-mcp.mcpb \
  --title "UML-MCP Desktop Extension v1.3.0" \
  --notes "## 🚀 One-Click Installation for Claude Desktop

Download \`uml-mcp.mcpb\` and double-click to install, or import via Claude Desktop → Settings → Extensions.

### Features
- 13 diagram generation tools (UML, Mermaid, D2, Graphviz, ERD)
- 3 prompt templates
- Cross-platform support (Windows, macOS, Linux)
- Automatic dependency management

### Installation
1. Download \`uml-mcp.mcpb\`
2. Double-click the file OR import via Claude Desktop → Settings → Extensions
3. Configure output directory
4. Start generating diagrams!

### What's New in v1.3.0
- [List your changes here]

See [DESKTOP_EXTENSION_GUIDE.md](https://github.com/ChistokhinSV/uml-mcp/blob/main/DESKTOP_EXTENSION_GUIDE.md) for detailed usage instructions."
```

#### Option B: Using GitHub Web UI

1. Go to https://github.com/ChistokhinSV/uml-mcp/releases
2. Click "Draft a new release"
3. **Tag:** Select or create `v1.3.0`
4. **Title:** `UML-MCP Desktop Extension v1.3.0`
5. **Description:** Copy the release notes from Option A above
6. **Attach files:** Upload `uml-mcp.mcpb`
7. Click "Publish release"

### 5. Verify the Release

1. Go to https://github.com/ChistokhinSV/uml-mcp/releases
2. Verify the release is published
3. Verify `uml-mcp.mcpb` is attached and downloadable
4. Test downloading and installing the extension:
   - Download `uml-mcp.mcpb`
   - Double-click to install in Claude Desktop
   - Verify it installs correctly
   - Test generating a simple diagram

### 6. Announce (Optional)

- Update project README if needed
- Announce on social media, forums, etc.
- Update documentation if there are new features

## Cross-Platform Compatibility

**Important:** The `.mcpb` file is cross-platform compatible. A single build works on:
- ✅ Windows
- ✅ macOS
- ✅ Linux

You only need to create ONE `.mcpb` file per release, regardless of platform.

## Troubleshooting

### Build fails with encoding error
If you see `UnicodeEncodeError` on Windows:
- Use `python build.py` instead of the PowerShell script
- The Python script handles encoding correctly

### .mcpb file is too large (>10 MB)
Check if you're accidentally including:
- `__pycache__` directories
- `.pyc` files
- Virtual environment directories
- Build artifacts

These should be excluded by the build script.

### .mcpb file won't install in Claude Desktop
1. Verify the file is a valid ZIP archive: `unzip -t uml-mcp.mcpb`
2. Check that `manifest.json` is at the root level
3. Ensure all required files are present

## Release Cadence

Recommended release schedule:
- **Major releases (1.x.0)**: New features, breaking changes
- **Minor releases (x.1.0)**: New features, enhancements
- **Patch releases (x.x.1)**: Bug fixes, documentation updates

## Post-Release Cleanup

After creating a release:
```bash
# Clean up the .mcpb file (it's in .gitignore)
rm uml-mcp.mcpb

# Optional: Create a new branch for the next version
git checkout -b v1.4.0-dev
```

## Questions?

- File an issue on GitHub
- Check the [DESKTOP_EXTENSION_GUIDE.md](DESKTOP_EXTENSION_GUIDE.md) for technical details
- Review Anthropic's [Desktop Extensions documentation](https://www.anthropic.com/engineering/desktop-extensions)
