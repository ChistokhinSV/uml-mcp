#!/bin/bash
# Build script for UML-MCP Claude Desktop Extension

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
OUTPUT_FILE="$PROJECT_ROOT/uml-mcp.mcpb"

echo "Building UML-MCP Desktop Extension..."
echo "Project root: $PROJECT_ROOT"
echo "Output file: $OUTPUT_FILE"

# Check if manifest.json exists
if [ ! -f "$SCRIPT_DIR/manifest.json" ]; then
    echo "Error: manifest.json not found in $SCRIPT_DIR"
    exit 1
fi

# Remove old package if it exists
if [ -f "$OUTPUT_FILE" ]; then
    echo "Removing old package..."
    rm "$OUTPUT_FILE"
fi

# Create temporary build directory
BUILD_DIR=$(mktemp -d)
echo "Using temporary build directory: $BUILD_DIR"

# Copy extension files
echo "Copying extension files..."
cp "$SCRIPT_DIR/manifest.json" "$BUILD_DIR/"
if [ -f "$SCRIPT_DIR/icon.png" ]; then
    cp "$SCRIPT_DIR/icon.png" "$BUILD_DIR/"
fi

# Copy server files
echo "Copying server files..."
cp "$PROJECT_ROOT/mcp_server.py" "$BUILD_DIR/"
cp "$PROJECT_ROOT/pyproject.toml" "$BUILD_DIR/"

# Copy package directories
for dir in mcp_core kroki mermaid plantuml D2 ai_uml; do
    if [ -d "$PROJECT_ROOT/$dir" ]; then
        echo "Copying $dir/..."
        cp -r "$PROJECT_ROOT/$dir" "$BUILD_DIR/"
    fi
done

# Create the .mcpb package (it's just a ZIP file)
echo "Creating .mcpb package..."
cd "$BUILD_DIR"
zip -r "$OUTPUT_FILE" . -x "*.pyc" -x "__pycache__/*" -x "*.git*" -x "*.DS_Store"

# Cleanup
cd "$PROJECT_ROOT"
rm -rf "$BUILD_DIR"

# Verify the package
if [ -f "$OUTPUT_FILE" ]; then
    SIZE=$(du -h "$OUTPUT_FILE" | cut -f1)
    echo "✓ Package created successfully: $OUTPUT_FILE ($SIZE)"
    echo ""
    echo "To install:"
    echo "  1. Open Claude Desktop"
    echo "  2. Go to Settings → Extensions"
    echo "  3. Click 'Import Extension'"
    echo "  4. Select: $OUTPUT_FILE"
    echo ""
    echo "Or simply double-click the file to install."
else
    echo "✗ Error: Failed to create package"
    exit 1
fi
