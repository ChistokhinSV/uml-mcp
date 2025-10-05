"""
MCP resources for diagram information
"""
import logging
from typing import Dict, List, Any, Optional, Callable, TypeVar, cast

from mcp_core.server.fastmcp_wrapper import FastMCP
from ..core.config import MCP_SETTINGS
from kroki.kroki_templates import DiagramTemplates, DiagramExamples

logger = logging.getLogger(__name__)

# Store for registered resources when using decorator pattern
_registered_resources: Dict[str, Dict[str, Any]] = {}

F = TypeVar('F', bound=Callable[..., Any])

def mcp_resource(
    uri: str,
    description: Optional[str] = None,
    category: str = "default"
) -> Callable[[F], F]:
    """
    Decorator for registering a function as an MCP resource.
    
    Args:
        uri: Resource URI
        description: Resource description (defaults to function docstring if not provided)
        category: Resource category for organization
        
    Returns:
        Decorated function
    
    Example:
        @mcp_resource("uml://types", description="Get available diagram types")
        def get_diagram_types():
            # Implementation
            return {"class": {...}, "sequence": {...}}
    """
    def decorator(func: F) -> F:
        func_doc = func.__doc__ or ""
        func_description = description or func_doc.split('\n')[0] if func_doc else ""
        
        # Store resource metadata
        _registered_resources[uri] = {
            "function": func,
            "uri": uri,
            "description": func_description,
            "category": category
        }
        
        # Return function unchanged
        return cast(F, func)
    
    return decorator

# Define resources using decorators
@mcp_resource("uml://types", description="Get available diagram types")
def get_diagram_types():
    """Get available diagram types"""
    types = {}
    for name, config in MCP_SETTINGS.diagram_types.items():
        types[name] = {
            "backend": config.backend,
            "description": config.description,
            "formats": config.formats
        }
    return types

@mcp_resource("uml://templates", description="Get diagram templates for different diagram types")
def get_diagram_templates():
    """Get diagram templates for different diagram types"""
    templates = {}
    for name in MCP_SETTINGS.diagram_types:
        templates[name] = DiagramTemplates.get_template(name)
    return templates

@mcp_resource("uml://examples", description="Get diagram examples for different diagram types")
def get_diagram_examples():
    """Get diagram examples for different diagram types"""
    examples = {}
    for name in MCP_SETTINGS.diagram_types:
        examples[name] = DiagramExamples.get_example(name)
    return examples

@mcp_resource("uml://formats", description="Get supported output formats for each diagram type")
def get_output_formats():
    """Get supported output formats for each diagram type"""
    formats = {}
    for name, config in MCP_SETTINGS.diagram_types.items():
        formats[name] = config.formats
    return formats

@mcp_resource("uml://server-info", description="Get MCP server information")
def get_server_info():
    """Get MCP server information"""
    return {
        "server_name": MCP_SETTINGS.server_name,
        "version": MCP_SETTINGS.version,
        "description": MCP_SETTINGS.description,
        "tools": MCP_SETTINGS.tools,
        "prompts": MCP_SETTINGS.prompts,
        "kroki_server": MCP_SETTINGS.kroki_server,
        "plantuml_server": MCP_SETTINGS.plantuml_server
    }

def register_resources_with_server(server: FastMCP) -> List[str]:
    """
    Register all decorated resources with the MCP server
    
    Args:
        server: The MCP server instance
        
    Returns:
        List of registered resource URIs
    """
    logger.info(f"Registering {len(_registered_resources)} resources with the MCP server")
    
    registered_resource_uris = []
    
    for uri, resource_info in _registered_resources.items():
        func = resource_info["function"]
        
        # Register with server using resource decorator
        resource_decorator = server.resource(uri)
        resource_decorator(func)
        
        registered_resource_uris.append(uri)
        logger.debug(f"Registered resource: {uri}")
    
    return registered_resource_uris

def register_diagram_resources(server: FastMCP) -> List[str]:
    """
    Register diagram resources with the MCP server
    
    Args:
        server: The MCP server instance
        
    Returns:
        List of registered resource names
    """
    logger.info("Registering diagram resources")
    
    # Register all resources that were decorated with @mcp_resource
    registered_resources = register_resources_with_server(server)
    
    # Store registered resources in MCP_SETTINGS
    MCP_SETTINGS.resources = registered_resources
    
    logger.info("Diagram resources registered successfully")
    
    return registered_resources

def get_resource_registry() -> Dict[str, Dict[str, Any]]:
    """
    Get the registry of all resources registered with the decorator
    
    Returns:
        Dictionary of resource metadata
    """
    return _registered_resources
