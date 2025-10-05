# Build script for UML-MCP Claude Desktop Extension (Windows)
# PowerShell version

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir
$OutputFile = Join-Path $ProjectRoot "uml-mcp.mcpb"

Write-Host "Building UML-MCP Desktop Extension..." -ForegroundColor Green
Write-Host "Project root: $ProjectRoot"
Write-Host "Output file: $OutputFile"

# Check if manifest.json exists
$ManifestPath = Join-Path $ScriptDir "manifest.json"
if (-not (Test-Path $ManifestPath)) {
    Write-Host "Error: manifest.json not found in $ScriptDir" -ForegroundColor Red
    exit 1
}

# Remove old package if it exists
if (Test-Path $OutputFile) {
    Write-Host "Removing old package..."
    Remove-Item $OutputFile
}

# Create temporary build directory
$BuildDir = Join-Path $env:TEMP "uml-mcp-build-$(Get-Random)"
New-Item -ItemType Directory -Path $BuildDir | Out-Null
Write-Host "Using temporary build directory: $BuildDir"

try {
    # Copy extension files
    Write-Host "Copying extension files..."
    Copy-Item $ManifestPath -Destination $BuildDir

    $IconPath = Join-Path $ScriptDir "icon.png"
    if (Test-Path $IconPath) {
        Copy-Item $IconPath -Destination $BuildDir
    }

    # Copy server files
    Write-Host "Copying server files..."
    Copy-Item (Join-Path $ProjectRoot "mcp_server.py") -Destination $BuildDir
    Copy-Item (Join-Path $ProjectRoot "pyproject.toml") -Destination $BuildDir

    # Copy package directories
    $Packages = @("mcp_core", "kroki", "mermaid", "plantuml", "D2", "ai_uml")
    foreach ($pkg in $Packages) {
        $PkgPath = Join-Path $ProjectRoot $pkg
        if (Test-Path $PkgPath) {
            Write-Host "Copying $pkg/..."
            Copy-Item $PkgPath -Destination $BuildDir -Recurse
        }
    }

    # Create the .mcpb package (it's just a ZIP file)
    Write-Host "Creating .mcpb package..."

    # Use .NET compression
    Add-Type -AssemblyName System.IO.Compression.FileSystem

    # Remove existing archive if it exists
    if (Test-Path $OutputFile) {
        Remove-Item $OutputFile
    }

    [System.IO.Compression.ZipFile]::CreateFromDirectory($BuildDir, $OutputFile)

    # Verify the package
    if (Test-Path $OutputFile) {
        $Size = (Get-Item $OutputFile).Length / 1MB
        Write-Host "✓ Package created successfully: $OutputFile ($($Size.ToString('0.00')) MB)" -ForegroundColor Green
        Write-Host ""
        Write-Host "To install:" -ForegroundColor Cyan
        Write-Host "  1. Open Claude Desktop"
        Write-Host "  2. Go to Settings → Extensions"
        Write-Host "  3. Click 'Import Extension'"
        Write-Host "  4. Select: $OutputFile"
        Write-Host ""
        Write-Host "Or simply double-click the file to install."
    }
    else {
        Write-Host "✗ Error: Failed to create package" -ForegroundColor Red
        exit 1
    }
}
finally {
    # Cleanup
    if (Test-Path $BuildDir) {
        Remove-Item $BuildDir -Recurse -Force
    }
}
