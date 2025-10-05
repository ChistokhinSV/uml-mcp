#!/usr/bin/env python3
"""
UML-MCP-Server: UML diagram generation server with MCP interface

This module provides the main entry point for the MCP server that generates UML
diagrams through the Model Context Protocol (MCP).
"""

import os
import sys
import logging
import argparse
import datetime
from rich.console import Console
from rich.logging import RichHandler
from rich.panel import Panel
from rich.table import Table

# Configure rich console
console = Console()

# Parse command line arguments
def parse_args():
    parser = argparse.ArgumentParser(description="UML-MCP Diagram Generation Server")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Server host (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8000, help="Server port (default: 8000)")
    parser.add_argument("--transport", type=str, choices=["stdio", "http"], default="stdio", 
                        help="Transport protocol (default: stdio)")
    parser.add_argument("--list-tools", action="store_true", help="List available tools and exit")
    return parser.parse_args()

# Configure logging based on arguments
def setup_logging(debug=False):
    level = logging.DEBUG if debug else logging.INFO
    
    # Create logs directory if it doesn't exist
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Generate log filename with today's date
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    log_file = os.path.join(log_dir, f"uml_mcp_server_{date_str}.log")
    
    # Configure file handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(level)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    
    # Configure console handler
    console_handler = RichHandler(rich_tracebacks=True)
    console_handler.setLevel(level)
    
    # Configure root logger
    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[console_handler]
    )
    
    # Get logger and add file handler
    logger = logging.getLogger()
    logger.addHandler(file_handler)
    
    return logging.getLogger(__name__)

# Centralized error handling for imports
def safe_import(module_name, display_name=None):
    try:
        return __import__(module_name)
    except ImportError as e:
        display_name = display_name or module_name
        console.print(f"[bold red]Error importing {display_name}:[/bold red] {str(e)}")
        return None

# Function to display the tools, prompts, and resources
def display_tools_and_resources(mcp_settings):
    """Display information about all available tools, prompts, and resources in the MCP server"""
    # Display tools
    display_tools(mcp_settings)
    
    # Display prompts
    display_prompts(mcp_settings)
    
    # Display resources
    display_resources(mcp_settings)

def display_tools(mcp_settings):
    """Display information about available tools in the MCP server"""
    # Create tools table
    tools_table = Table(title="[bold blue]Available UML-MCP Tools[/bold blue]")
    tools_table.add_column("Tool Name", style="cyan")
    tools_table.add_column("Description", style="green")
    tools_table.add_column("Parameters", style="yellow")
    
    # Import tool registry if available
    try:
        from mcp_core.tools.tool_decorator import get_tool_registry
        tool_registry = get_tool_registry()
        
        if tool_registry:
            # Add rows for each tool from registry
            for tool_name, tool_info in tool_registry.items():
                # Skip internal tools
                if tool_name == 'tool_function':
                    continue
                
                # Get description and parameters
                description = tool_info.get("description", "No description available")
                
                # Format parameters
                params = tool_info.get("parameters", {})
                param_str = ", ".join([f"{name}: {info['type']}" for name, info in params.items()])
                
                tools_table.add_row(tool_name, description, param_str)
        else:
            # Fallback to old method if registry not available
            _display_tools_fallback(mcp_settings, tools_table)
    except ImportError:
        # Fallback to old method if decorator system not available
        _display_tools_fallback(mcp_settings, tools_table)
    
    console.print(tools_table)

def _display_tools_fallback(mcp_settings, tools_table):
    """Fallback method to display tools if decorator system is not available"""
    # Get tool names from settings
    tool_names = getattr(mcp_settings, 'tools', [])
    
    if tool_names:
        # Tool descriptions dictionary
        tool_descriptions = {
            "generate_uml": "Generate any UML diagram based on diagram type",
            "generate_class_diagram": "Generate UML class diagram from PlantUML code",
            "generate_sequence_diagram": "Generate UML sequence diagram from PlantUML code",
            "generate_activity_diagram": "Generate UML activity diagram from PlantUML code",
            "generate_usecase_diagram": "Generate UML use case diagram from PlantUML code",
            "generate_state_diagram": "Generate UML state diagram from PlantUML code",
            "generate_component_diagram": "Generate UML component diagram from PlantUML code",
            "generate_deployment_diagram": "Generate UML deployment diagram from PlantUML code",
            "generate_object_diagram": "Generate UML object diagram from PlantUML code",
            "generate_mermaid_diagram": "Generate diagrams using Mermaid syntax",
            "generate_d2_diagram": "Generate diagrams using D2 syntax",
            "generate_graphviz_diagram": "Generate diagrams using Graphviz DOT syntax",
            "generate_erd_diagram": "Generate Entity-Relationship diagrams"
        }
        
        # Tool parameters dictionary
        tool_parameters = {
            "generate_uml": "diagram_type: str, code: str, output_dir: str",
            "generate_class_diagram": "code: str, output_dir: str",
            "generate_sequence_diagram": "code: str, output_dir: str",
            "generate_activity_diagram": "code: str, output_dir: str",
            "generate_usecase_diagram": "code: str, output_dir: str",
            "generate_state_diagram": "code: str, output_dir: str",
            "generate_component_diagram": "code: str, output_dir: str",
            "generate_deployment_diagram": "code: str, output_dir: str",
            "generate_object_diagram": "code: str, output_dir: str",
            "generate_mermaid_diagram": "code: str, output_dir: str",
            "generate_d2_diagram": "code: str, output_dir: str",
            "generate_graphviz_diagram": "code: str, output_dir: str",
            "generate_erd_diagram": "code: str, output_dir: str"
        }
        
        # Add rows for each tool
        for tool_name in tool_names:
            # Skip the tool_function which is not a user-facing tool
            if tool_name == 'tool_function':
                continue
            
            # Get description and parameters or use defaults
            description = tool_descriptions.get(tool_name, "Generate diagrams based on text descriptions")
            parameters = tool_parameters.get(tool_name, "No parameters info")
            
            tools_table.add_row(tool_name, description, parameters)
    else:
        tools_table.add_row("No tools found", "Check server configuration", "")

def display_prompts(mcp_settings):
    """Display information about available prompts in the MCP server"""
    # Create prompts table
    prompts_table = Table(title="[bold blue]Available Prompts[/bold blue]")
    prompts_table.add_column("Prompt Name", style="cyan")
    prompts_table.add_column("Description", style="green")
    
    # Import prompt registry if available
    try:
        from mcp_core.prompts.diagram_prompts import get_prompt_registry
        prompt_registry = get_prompt_registry()
        
        if prompt_registry:
            # Add rows for each prompt from registry
            for prompt_name, prompt_info in prompt_registry.items():
                # Get description
                description = prompt_info.get("description", "No description available")
                prompts_table.add_row(prompt_name, description)
        else:
            # Fallback to old method if registry not available
            _display_prompts_fallback(mcp_settings, prompts_table)
    except ImportError:
        # Fallback to old method if decorator system not available
        _display_prompts_fallback(mcp_settings, prompts_table)
    
    console.print(prompts_table)

def _display_prompts_fallback(mcp_settings, prompts_table):
    """Fallback method to display prompts if decorator system is not available"""
    # Get prompt names from settings
    prompt_names = getattr(mcp_settings, 'prompts', [])
    
    if prompt_names:
        # Prompt descriptions dictionary
        prompt_descriptions = {
            "class_diagram": "Create a UML class diagram showing classes, attributes, methods, and relationships",
            "sequence_diagram": "Create a UML sequence diagram showing interactions between objects over time",
            "activity_diagram": "Create a UML activity diagram showing workflows and business processes"
        }
        
        # Add rows for each prompt
        for prompt_name in prompt_names:
            # Get description or use default
            description = prompt_descriptions.get(prompt_name, "Generate UML diagrams")
            prompts_table.add_row(prompt_name, description)
    else:
        prompts_table.add_row("No prompts found", "Check server configuration")

def display_resources(mcp_settings):
    """Display information about available resources in the MCP server"""
    # Create resources table
    resources_table = Table(title="[bold blue]Available Resources[/bold blue]")
    resources_table.add_column("Resource URI", style="cyan")
    resources_table.add_column("Description", style="green")
    
    # Import resource registry if available
    try:
        from mcp_core.resources.diagram_resources import get_resource_registry
        resource_registry = get_resource_registry()
        
        if resource_registry:
            # Add rows for each resource from registry
            for resource_uri, resource_info in resource_registry.items():
                # Get description
                description = resource_info.get("description", "No description available")
                resources_table.add_row(resource_uri, description)
        else:
            # Fallback to old method if registry not available
            _display_resources_fallback(mcp_settings, resources_table)
    except ImportError:
        # Fallback to old method if decorator system not available
        _display_resources_fallback(mcp_settings, resources_table)
    
    console.print(resources_table)

def _display_resources_fallback(mcp_settings, resources_table):
    """Fallback method to display resources if decorator system is not available"""
    # Get resource names from settings
    resource_names = getattr(mcp_settings, 'resources', [])
    
    if resource_names:
        # Resource descriptions dictionary
        resource_descriptions = {
            "uml://types": "List of available UML diagram types",
            "uml://templates": "Templates for creating UML diagrams",
            "uml://examples": "Example UML diagrams for reference",
            "uml://formats": "Supported output formats for diagrams",
            "uml://server-info": "Information about the UML-MCP server"
        }
        
        # Add rows for each resource
        for resource_name in resource_names:
            # Get description or use default
            description = resource_descriptions.get(resource_name, "Resource information")
            resources_table.add_row(resource_name, description)
    else:
        resources_table.add_row("No resources found", "Check server configuration")

def main():
    # Import datetime here to avoid circular import
    import datetime
    
    # Parse arguments and set up logging
    args = parse_args()
    logger = setup_logging(args.debug)
    
    logger.info(f"Starting UML-MCP Server with transport: {args.transport}")
    
    # Check required modules
    required_modules = {
        "mcp.server": "MCP Server",
        "kroki.kroki": "Kroki",
        "plantuml": "PlantUML",
        "mermaid.mermaid": "Mermaid",
        "D2.run_d2": "D2"
    }
    
    missing_modules = []
    for module_name, display_name in required_modules.items():
        if not safe_import(module_name, display_name):
            missing_modules.append(display_name)

    if missing_modules:
        console.print(f"[bold red]Error:[/bold red] Missing required modules: {', '.join(missing_modules)}")
        console.print("Please ensure all project components are correctly installed.")
        sys.exit(1)

    # Import core server
    try:
        from mcp_core.core.server import create_mcp_server, get_mcp_server, start_server
        from mcp_core.core.config import MCP_SETTINGS
        
        # Update settings from command line args if applicable
        if hasattr(MCP_SETTINGS, 'update_from_args'):
            MCP_SETTINGS.update_from_args(args)
        
        # Check if we need to create a new server or get an existing one
        # Note: get_mcp_server() already registers components when first called
        server = get_mcp_server()
        
        # Display server info (after tools and prompts are registered)
        console.print(Panel(f"[bold green]UML-MCP Server v{MCP_SETTINGS.version}[/bold green]"))
        
        # Create a table for server info
        table = Table(title="Server Configuration")
        table.add_column("Setting", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Server Name", MCP_SETTINGS.server_name)
        table.add_row("Transport", args.transport)
        table.add_row("Available Tools", str(len(MCP_SETTINGS.tools)))
        table.add_row("Available Prompts", str(len(MCP_SETTINGS.prompts)))
        table.add_row("Available Resources", str(len(MCP_SETTINGS.resources)))
        if args.transport == "http":
            table.add_row("Host", args.host)
            table.add_row("Port", str(args.port))
        
        console.print(table)
        
        # Display tools list if requested
        list_tools = args.list_tools or os.environ.get("LIST_TOOLS", "").lower() == "true"
        if list_tools:
            display_tools_and_resources(MCP_SETTINGS)
            return
        
        # Start MCP server
        start_server(transport=args.transport, host=args.host, port=args.port)
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.critical(f"Server error: {str(e)}", exc_info=True)
    finally:
        logger.info("Server shut down")

if __name__ == "__main__":
    main()
