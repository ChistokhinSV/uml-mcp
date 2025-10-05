#!/usr/bin/env python3
"""
UML Diagram Generator - Simplified MCP Server

A minimal MCP server for generating UML diagrams using FastMCP, Typer, and Rich.
"""

# Add lib directory to path (for bundled dependencies in Desktop Extension)
import sys
import os
from pathlib import Path

_script_dir = Path(__file__).parent
_lib_dir = _script_dir / "lib"
if _lib_dir.exists() and str(_lib_dir) not in sys.path:
    sys.path.insert(0, str(_lib_dir))

# Platform validation for bundled dependencies
if _lib_dir.exists():
    import platform
    current_platform = platform.system()

    # Check for platform-specific binary files to detect build platform
    sample_binaries = list(_lib_dir.glob("**/*.so")) + list(_lib_dir.glob("**/*.pyd"))

    if sample_binaries:
        has_linux_binaries = any(f.suffix == ".so" for f in sample_binaries)
        has_windows_binaries = any(f.suffix == ".pyd" for f in sample_binaries)

        if current_platform == "Windows" and has_linux_binaries and not has_windows_binaries:
            print(f"[bold red]ERROR: Platform mismatch detected![/bold red]", file=sys.stderr)
            print(f"[yellow]You are running on Windows but this extension was built for Linux.[/yellow]", file=sys.stderr)
            print(f"[yellow]Please download the correct version:[/yellow]", file=sys.stderr)
            print(f"  - Windows: uml-mcp-windows.mcpb", file=sys.stderr)
            print(f"  - Linux/macOS: uml-mcp-linux.mcpb", file=sys.stderr)
            sys.exit(1)
        elif current_platform == "Linux" and has_windows_binaries and not has_linux_binaries:
            print(f"[bold red]ERROR: Platform mismatch detected![/bold red]", file=sys.stderr)
            print(f"[yellow]You are running on Linux but this extension was built for Windows.[/yellow]", file=sys.stderr)
            print(f"[yellow]Please download the correct version:[/yellow]", file=sys.stderr)
            print(f"  - Windows: uml-mcp-windows.mcpb", file=sys.stderr)
            print(f"  - Linux/macOS: uml-mcp-linux.mcpb", file=sys.stderr)
            sys.exit(1)

import zlib
import base64
from typing import Dict, Any

import typer
from rich import print
from rich.console import Console
from rich.table import Table

from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent, PromptMessage, GetPromptResult

# Configuration: Use PlantUML server (can be overridden with env var)
PLANTUML_SERVER = os.environ.get("PLANTUML_SERVER", "http://www.plantuml.com/plantuml")


def encode_plantuml(text: str) -> str:
    """Encode PlantUML text using zlib and base64."""
    compressed = zlib.compress(text.encode("utf-8"))
    # Strip the first two and last four bytes per PlantUML spec
    return base64.urlsafe_b64encode(compressed[2:-4]).decode("utf-8")


def generate_diagram(code: str, fmt: str = "svg") -> Dict[str, Any]:
    """Generate a diagram URL using the PlantUML server."""
    encoded = encode_plantuml(code)
    url = f"{PLANTUML_SERVER}/{fmt}/{encoded}"
    return {"url": url, "code": code}


# Create a FastMCP server instance
server = FastMCP("UML Diagram Generator")


# Register an MCP tool to generate a UML diagram
@server.tool(name="generate_uml", description="Generate a UML diagram using PlantUML")
def generate_uml(diagram_type: str, code: str) -> Dict[str, Any]:
    # For simplicity, the diagram_type parameter is not used.
    return generate_diagram(code)


# Register an MCP resource to expose server info
@server.resource("uml://info")
def get_info() -> Dict[str, Any]:
    return {"server": "UML Diagram Generator", "version": "1.0"}


# Register an MCP prompt with a simple template
@server.prompt(name="simple_prompt", description="Simple prompt for diagram generation")
def simple_prompt(context: Dict[str, Any]) -> GetPromptResult:
    code = context.get("code", "@startuml\nAlice -> Bob: Hello\n@enduml")
    return GetPromptResult(
        description="Simple prompt for UML diagram",
        messages=[PromptMessage(role="user", content=TextContent(text=code))]
    )


# Set up the CLI using Typer and Rich
cli = typer.Typer()


@cli.command()
def run():
    """Run the MCP server using stdio transport."""
    # Don't print to stdout - it interferes with MCP JSON-RPC protocol
    server.run()


@cli.command()
def info():
    """Display server information."""
    console = Console()
    table = Table("Property", "Value")
    table.add_row("Server", "UML Diagram Generator")
    table.add_row("Version", "1.0")
    console.print(table)


if __name__ == "__main__":
    cli()
