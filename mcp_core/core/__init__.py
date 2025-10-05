"""
MCP Core module initialization.
This ensures the mcp.core module is properly recognized.
"""
from .config import MCP_SETTINGS
from .utils import generate_diagram
from .server import create_mcp_server, get_mcp_server, start_server
