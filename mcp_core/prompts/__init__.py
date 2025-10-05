"""
MCP prompts for diagram generation
"""
from .diagram_prompts import (
    uml_diagram_prompt,
    class_diagram_prompt,
    sequence_diagram_prompt,
    activity_diagram_prompt,
    usecase_diagram_prompt,
    mcp_prompt,
    get_prompt_registry
)

__all__ = [
    'uml_diagram_prompt',
    'class_diagram_prompt',
    'sequence_diagram_prompt',
    'activity_diagram_prompt',
    'usecase_diagram_prompt',
    'mcp_prompt',
    'get_prompt_registry'
]