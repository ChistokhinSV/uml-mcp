"""
MCP tools decorator system for simplified tool registration
"""

import logging
import inspect
import functools
from typing import Dict, Any, List, Callable, Optional, TypeVar, cast

# Import FastMCP with error handling to support testing environments
try:
    from mcp.server import FastMCP
except ImportError:
    # Mock FastMCP for testing environments
    class FastMCP:
        def __init__(self):
            self._tools = {}
        
        def tool(self, *args, **kwargs):
            if args and callable(args[0]):
                # Called as a decorator with no arguments
                func = args[0]
                self._tools[func.__name__] = func
                return func
            else:
                # Called with arguments or no arguments
                def decorator(func):
                    self._tools[func.__name__] = func
                    return func
                return decorator

logger = logging.getLogger(__name__)

# Store for registered tools when using the decorator pattern
_registered_tools: Dict[str, Dict[str, Any]] = {}

F = TypeVar('F', bound=Callable[..., Any])

def mcp_tool(
    name: Optional[str] = None,
    description: Optional[str] = None,
    category: str = "default",
    required_params: Optional[List[str]] = None,
    example: Optional[str] = None
) -> Callable[[F], F]:
    """
    Decorator for registering a function as an MCP tool.
    
    Args:
        name: Tool name (defaults to function name if not provided)
        description: Tool description (defaults to function docstring if not provided)
        category: Tool category for organization
        required_params: List of required parameter names
        example: Example usage of the tool
        
    Returns:
        Decorated function
    
    Example:
        @mcp_tool(description="Generate a class diagram", category="uml")
        def generate_class_diagram(code: str, output_dir: str) -> Dict[str, Any]:
            # Implementation
            return {"code": code, "url": "..."}
    """
    def decorator(func: F) -> F:
        func_name = name or func.__name__
        func_doc = inspect.getdoc(func) or ""
        func_description = description or func_doc.split('\n')[0] if func_doc else ""
        
        # Get parameter annotations from function signature
        sig = inspect.signature(func)
        param_info = {}
        
        for param_name, param in sig.parameters.items():
            param_type = param.annotation if param.annotation is not inspect.Parameter.empty else None
            param_default = None if param.default is inspect.Parameter.empty else param.default
            
            param_info[param_name] = {
                "type": param_type.__name__ if hasattr(param_type, "__name__") else str(param_type),
                "required": param.default is inspect.Parameter.empty,
                "default": param_default
            }
        
        # Store tool metadata
        _registered_tools[func_name] = {
            "function": func,
            "name": func_name,
            "description": func_description,
            "category": category,
            "parameters": param_info,
            "required_params": required_params or [p for p, info in param_info.items() if info["required"]],
            "example": example,
            "return_type": sig.return_annotation if sig.return_annotation is not inspect.Parameter.empty else None
        }
        
        # Return function unchanged
        return cast(F, func)
    
    return decorator

def register_tools_with_server(server: FastMCP) -> List[str]:
    """
    Register all decorated tools with the MCP server
    
    Args:
        server: The MCP server instance
        
    Returns:
        List of registered tool names
    """
    logger.info(f"Registering {len(_registered_tools)} tools with the MCP server")
    
    registered_tools = []
    
    for tool_name, tool_info in _registered_tools.items():
        func = tool_info["function"]
        
        # Register with server (handle different server APIs)
        try:
            # First try with name parameter (new style)
            tool_decorator = server.tool(
                name=tool_name, 
                description=tool_info["description"]
            )
            tool_decorator(func)
        except TypeError:
            try:
                # Try just passing the description (alternate style)
                tool_decorator = server.tool(tool_info["description"])
                tool_decorator(func)
            except TypeError:
                # Fallback to simple decorator with no args (basic style)
                server.tool(func)
                
                # If that didn't throw an error but we need to rename the function
                if tool_name != func.__name__:
                    # Use the _tools dictionary directly if we can access it
                    if hasattr(server, "_tools"):
                        server._tools[tool_name] = server._tools.pop(func.__name__, func)
                    else:
                        logger.warning(f"Could not rename tool '{func.__name__}' to '{tool_name}' - server API doesn't support it")
        
        registered_tools.append(tool_name)
        logger.debug(f"Registered tool: {tool_name}")
    
    return registered_tools

def get_tool_registry() -> Dict[str, Dict[str, Any]]:
    """
    Get the registry of all tools registered with the decorator
    
    Returns:
        Dictionary of tool metadata
    """
    return _registered_tools

def get_tool_categories() -> Dict[str, List[str]]:
    """
    Get tools organized by category
    
    Returns:
        Dictionary mapping categories to tool names
    """
    categories = {}
    
    for tool_name, tool_info in _registered_tools.items():
        category = tool_info["category"]
        if category not in categories:
            categories[category] = []
        
        categories[category].append(tool_name)
    
    return categories

def clear_tool_registry():
    """
    Clear the tool registry (mainly for testing)
    """
    _registered_tools.clear()