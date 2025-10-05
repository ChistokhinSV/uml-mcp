#!/usr/bin/env python3
"""Build script for UML-MCP Claude Desktop Extension (cross-platform)"""

import os
import shutil
import tempfile
import zipfile
import subprocess
import sys
from pathlib import Path

def main():
    # Determine paths
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    output_file = project_root / "uml-mcp.mcpb"

    print("Building UML-MCP Desktop Extension...")
    print(f"Project root: {project_root}")
    print(f"Output file: {output_file}")

    # Check if manifest.json exists
    manifest_path = script_dir / "manifest.json"
    if not manifest_path.exists():
        print(f"Error: manifest.json not found in {script_dir}")
        return 1

    # Remove old package if it exists
    if output_file.exists():
        print("Removing old package...")
        output_file.unlink()

    # Create temporary build directory
    with tempfile.TemporaryDirectory(prefix="uml-mcp-build-") as build_dir:
        build_path = Path(build_dir)
        print(f"Using temporary build directory: {build_path}")

        # Copy extension files
        print("Copying extension files...")
        shutil.copy2(manifest_path, build_path / "manifest.json")

        icon_path = script_dir / "icon.png"
        if icon_path.exists():
            shutil.copy2(icon_path, build_path / "icon.png")

        # Copy bin directory with plantuml.jar
        bin_path = script_dir / "bin"
        if bin_path.exists():
            print("Copying bin directory (includes plantuml.jar)...")
            shutil.copytree(bin_path, build_path / "bin")

        # Copy server files
        print("Copying server files...")
        shutil.copy2(project_root / "mcp_server.py", build_path / "mcp_server.py")
        shutil.copy2(project_root / "pyproject.toml", build_path / "pyproject.toml")

        # Copy package directories
        packages = ["mcp_core", "kroki", "mermaid", "plantuml_local", "D2", "ai_uml"]
        for pkg in packages:
            pkg_path = project_root / pkg
            if pkg_path.exists():
                print(f"Copying {pkg}/...")
                shutil.copytree(pkg_path, build_path / pkg)

        # Install dependencies to lib directory within the extension
        print("\nInstalling Python dependencies...")
        lib_dir = build_path / "lib"
        lib_dir.mkdir(exist_ok=True)

        try:
            # Use pip to install dependencies to lib directory
            # Install with all transitive dependencies
            result = subprocess.run([
                sys.executable, "-m", "pip", "install",
                "--target", str(lib_dir),
                "--upgrade",
                "typer>=0.9.0",
                "rich>=13.6.0",
                "httpx>=0.24.1",
                "pydantic>=2.4.2",
                "fastmcp>=0.4.0",
                "mcp>=1.2.0"
            ], check=True, capture_output=True, text=True)

            if result.stdout:
                print(f"  {result.stdout.strip()}")
            print("[OK] Dependencies installed successfully")

            # Count installed packages
            package_count = len([d for d in lib_dir.iterdir() if d.is_dir() and not d.name.startswith('_')])
            print(f"  Installed {package_count} packages to lib/")

        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Failed to install dependencies: {e}")
            if e.stdout:
                print(f"  stdout: {e.stdout}")
            if e.stderr:
                print(f"  stderr: {e.stderr}")
            return 1

        # Create the .mcpb package (it's just a ZIP file)
        print("Creating .mcpb package...")
        with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(build_path):
                for file in files:
                    file_path = Path(root) / file
                    arcname = file_path.relative_to(build_path)
                    zipf.write(file_path, arcname)

        # Verify the package
        if output_file.exists():
            size_mb = output_file.stat().st_size / (1024 * 1024)
            print(f"\n[SUCCESS] Package created successfully: {output_file} ({size_mb:.2f} MB)")
            print("\nTo install:")
            print("  1. Open Claude Desktop")
            print("  2. Go to Settings -> Extensions")
            print("  3. Click 'Import Extension'")
            print(f"  4. Select: {output_file}")
            print("\nOr simply double-click the file to install.")
            return 0
        else:
            print("[ERROR] Failed to create package")
            return 1

if __name__ == "__main__":
    exit(main())
