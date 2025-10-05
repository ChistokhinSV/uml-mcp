"""
MCP tools for diagram generation using the decorator pattern
"""

import logging
import os
from typing import Dict, Any, List, Optional

from mcp_core.server.fastmcp_wrapper import FastMCP

# Import the tool decorator system
from .tool_decorator import mcp_tool, register_tools_with_server, get_tool_registry

# Import core utilities
from ..core.utils import generate_diagram
from ..core.config import MCP_SETTINGS

logger = logging.getLogger(__name__)

# Main UML generation tool
@mcp_tool(
    description="Generate any UML diagram based on diagram type",
    category="uml"
)
def generate_uml(diagram_type: str, code: str, output_dir: Optional[str] = None) -> Dict[str, Any]:
    """Generate a UML diagram using the specified diagram type.
    
    Args:
        diagram_type: Type of diagram (class, sequence, activity, etc.)
        code: The diagram code/description
        output_dir: Directory where to save the generated image (optional)
    
    Returns:
        Dictionary containing code, URL, and local file path
    """
    logger.info(f"Called generate_uml tool: type={diagram_type}, code length={len(code)}")
    
    # Validate diagram type
    valid_types = getattr(MCP_SETTINGS, 'diagram_types', {})
    if not valid_types:
        valid_types = {"class": "Class diagram", "sequence": "Sequence diagram"}
        
    if diagram_type.lower() not in valid_types:
        error_msg = f"Unsupported diagram type: {diagram_type}. Supported types: {', '.join(valid_types.keys())}"
        logger.error(error_msg)
        return {"error": error_msg}
    
    # Generate diagram - use default format "svg" to match tests
    return generate_diagram(diagram_type, code, "svg", output_dir)

# Class diagram tool
@mcp_tool(
    description="Generate UML class diagram from PlantUML code",
    category="uml",
    example="generate_class_diagram('@startuml\\nclass User\\n@enduml', './output')"
)
def generate_class_diagram(code: str, output_dir: Optional[str] = None) -> Dict[str, Any]:
    """Generate a UML class diagram from PlantUML code.
    
    Args:
        code: The PlantUML diagram code
        output_dir: Directory where to save the generated image (optional)
    
    Returns:
        Dictionary containing code, URL, and local file path
    """
    logger.info(f"Called generate_class_diagram tool: code length={len(code)}")
    return generate_uml("class", code, output_dir)

# Sequence diagram tool
@mcp_tool(
    description="Generate UML sequence diagram from PlantUML code",
    category="uml"
)
def generate_sequence_diagram(code: str, output_dir: Optional[str] = None) -> Dict[str, Any]:
    """Generate a UML sequence diagram from PlantUML code.
    
    Args:
        code: The PlantUML diagram code
        output_dir: Directory where to save the generated image (optional)
    
    Returns:
        Dictionary containing code, URL, and local file path
    """
    logger.info(f"Called generate_sequence_diagram tool: code length={len(code)}")
    return generate_uml("sequence", code, output_dir)

# Activity diagram tool
@mcp_tool(
    description="Generate UML activity diagram from PlantUML code",
    category="uml"
)
def generate_activity_diagram(code: str, output_dir: Optional[str] = None) -> Dict[str, Any]:
    """Generate a UML activity diagram from PlantUML code.
    
    Args:
        code: The PlantUML diagram code
        output_dir: Directory where to save the generated image (optional)
    
    Returns:
        Dictionary containing code, URL, and local file path
    """
    logger.info(f"Called generate_activity_diagram tool: code length={len(code)}")
    return generate_uml("activity", code, output_dir)

# Use case diagram tool
@mcp_tool(
    description="Generate UML use case diagram from PlantUML code",
    category="uml"
)
def generate_usecase_diagram(code: str, output_dir: Optional[str] = None) -> Dict[str, Any]:
    """Generate a UML use case diagram from PlantUML code.
    
    Args:
        code: The PlantUML diagram code
        output_dir: Directory where to save the generated image (optional)
    
    Returns:
        Dictionary containing code, URL, and local file path
    """
    logger.info(f"Called generate_usecase_diagram tool: code length={len(code)}")
    return generate_uml("usecase", code, output_dir)

# State diagram tool
@mcp_tool(
    description="Generate UML state diagram from PlantUML code",
    category="uml"
)
def generate_state_diagram(code: str, output_dir: Optional[str] = None) -> Dict[str, Any]:
    """Generate a UML state diagram from PlantUML code.
    
    Args:
        code: The PlantUML diagram code
        output_dir: Directory where to save the generated image (optional)
    
    Returns:
        Dictionary containing code, URL, and local file path
    """
    logger.info(f"Called generate_state_diagram tool: code length={len(code)}")
    return generate_uml("state", code, output_dir)

# Component diagram tool
@mcp_tool(
    description="Generate UML component diagram from PlantUML code",
    category="uml"
)
def generate_component_diagram(code: str, output_dir: Optional[str] = None) -> Dict[str, Any]:
    """Generate a UML component diagram from PlantUML code.
    
    Args:
        code: The PlantUML diagram code
        output_dir: Directory where to save the generated image (optional)
    
    Returns:
        Dictionary containing code, URL, and local file path
    """
    logger.info(f"Called generate_component_diagram tool: code length={len(code)}")
    return generate_uml("component", code, output_dir)

# Deployment diagram tool
@mcp_tool(
    description="Generate UML deployment diagram from PlantUML code",
    category="uml"
)
def generate_deployment_diagram(code: str, output_dir: Optional[str] = None) -> Dict[str, Any]:
    """Generate a UML deployment diagram from PlantUML code.
    
    Args:
        code: The PlantUML diagram code
        output_dir: Directory where to save the generated image (optional)
    
    Returns:
        Dictionary containing code, URL, and local file path
    """
    logger.info(f"Called generate_deployment_diagram tool: code length={len(code)}")
    return generate_uml("deployment", code, output_dir)

# Object diagram tool
@mcp_tool(
    description="Generate UML object diagram from PlantUML code",
    category="uml"
)
def generate_object_diagram(code: str, output_dir: Optional[str] = None) -> Dict[str, Any]:
    """Generate a UML object diagram from PlantUML code.
    
    Args:
        code: The PlantUML diagram code
        output_dir: Directory where to save the generated image (optional)
    
    Returns:
        Dictionary containing code, URL, and local file path
    """
    logger.info(f"Called generate_object_diagram tool: code length={len(code)}")
    return generate_uml("object", code, output_dir)

# Mermaid diagram tool
@mcp_tool(
    description="Generate diagrams using Mermaid syntax",
    category="other"
)
def generate_mermaid_diagram(code: str, output_dir: Optional[str] = None) -> Dict[str, Any]:
    """Generate a diagram using Mermaid syntax.
    
    Args:
        code: The Mermaid diagram code
        output_dir: Directory where to save the generated image (optional)
    
    Returns:
        Dictionary containing code, URL, and local file path
    """
    logger.info(f"Called generate_mermaid_diagram tool: code length={len(code)}")
    return generate_uml("mermaid", code, output_dir)

# D2 diagram tool
@mcp_tool(
    description="Generate diagrams using D2 syntax",
    category="other"
)
def generate_d2_diagram(code: str, output_dir: Optional[str] = None) -> Dict[str, Any]:
    """Generate a diagram using D2 syntax.
    
    Args:
        code: The D2 diagram code
        output_dir: Directory where to save the generated image (optional)
    
    Returns:
        Dictionary containing code, URL, and local file path
    """
    logger.info(f"Called generate_d2_diagram tool: code length={len(code)}")
    return generate_uml("d2", code, output_dir)

# Graphviz diagram tool
@mcp_tool(
    description="Generate diagrams using Graphviz DOT syntax",
    category="other"
)
def generate_graphviz_diagram(code: str, output_dir: Optional[str] = None) -> Dict[str, Any]:
    """Generate a diagram using Graphviz DOT syntax.
    
    Args:
        code: The Graphviz DOT code
        output_dir: Directory where to save the generated image (optional)
    
    Returns:
        Dictionary containing code, URL, and local file path
    """
    logger.info(f"Called generate_graphviz_diagram tool: code length={len(code)}")
    return generate_uml("graphviz", code, output_dir)

# ERD diagram tool
@mcp_tool(
    description="Generate Entity-Relationship diagrams",
    category="database"
)
def generate_erd_diagram(code: str, output_dir: Optional[str] = None) -> Dict[str, Any]:
    """Generate an Entity-Relationship diagram.
    
    Args:
        code: The ERD diagram code
        output_dir: Directory where to save the generated image (optional)
    
    Returns:
        Dictionary containing code, URL, and local file path
    """
    logger.info(f"Called generate_erd_diagram tool: code length={len(code)}")
    return generate_uml("erd", code, output_dir)

def register_diagram_tools(server: FastMCP) -> List[str]:
    """
    Register all diagram generation tools with the MCP server
    
    Args:
        server: The MCP server instance
        
    Returns:
        List of registered tool names
    """
    logger.info("Registering diagram tools")
    
    # Register all tools that were decorated with @mcp_tool
    registered_tools = register_tools_with_server(server)
    
    # Store registered tools in MCP_SETTINGS.tools (which is a standard attribute)
    MCP_SETTINGS.tools = registered_tools
    
    logger.info(f"Registered {len(registered_tools)} diagram tools successfully")
    logger.debug(f"Registered tools: {registered_tools}")
    
    return registered_tools

def get_tool_info() -> Dict[str, Dict[str, Any]]:
    """
    Get information about all registered tools
    
    Returns:
        Dictionary mapping tool names to their information
    """
    return get_tool_registry()
