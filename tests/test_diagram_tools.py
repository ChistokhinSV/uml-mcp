"""
Unit tests for diagram tool functions
"""
import pytest
from unittest.mock import patch, MagicMock

from mcp_core.tools.diagram_tools import register_diagram_tools

class TestDiagramTools:
    """Test suite for diagram tools functionality"""
    
    @pytest.fixture
    def mock_mcp_server(self):
        """Fixture to create a mock MCP server"""
        server = MagicMock()
        server.tool = MagicMock()
        return server
    
    def test_register_diagram_tools(self, mock_mcp_server):
        """Test that diagram tools are registered correctly"""
        # Call the register function
        register_diagram_tools(mock_mcp_server)
        
        # Verify that tool registration was called for each diagram type
        expected_tools = [
            "generate_uml",
            "generate_class_diagram",
            "generate_sequence_diagram",
            "generate_activity_diagram",
            "generate_usecase_diagram",
            "generate_state_diagram",
            "generate_component_diagram",
            "generate_deployment_diagram",
            "generate_object_diagram",
            "generate_mermaid_diagram",
            "generate_d2_diagram",
            "generate_graphviz_diagram",
            "generate_erd_diagram"
        ]
        
        # Check that each expected tool was registered
        for tool_name in expected_tools:
            # Find calls where the 'name' keyword argument matches the tool name
            matching_calls = [
                call for call in mock_mcp_server.tool.call_args_list
                if 'name' in call[1] and call[1]['name'] == tool_name
            ]

            assert len(matching_calls) > 0, f"Tool {tool_name} was not registered"

    # @patch("mcp.tools.diagram_tools.generate_diagram")
    # def test_generate_uml_tool(self, mock_generate_diagram, mock_mcp_server):
    #     """Test that the generate_uml tool works correctly"""
    #     # Register tools
    #     register_diagram_tools(mock_mcp_server)
        
    #     # Find the generate_uml tool function
    #     generate_uml_call = next(
    #         call for call in mock_mcp_server.tool.call_args_list 
    #         if len(call[0]) > 0 and call[0][0] == "generate_uml"
    #     )
        
    #     # Get the tool function (second positional argument)
    #     generate_uml_func = generate_uml_call[0][1]
        
    #     # Setup mock return value
    #     mock_generate_diagram.return_value = {
    #         "code": "test code",
    #         "url": "test url",
    #         "playground": "test playground",
    #         "local_path": "test local path"
    #     }
        
    #     # Call the tool function
    #     result = generate_uml_func(
    #         diagram_type="class",
    #         code="@startuml\nclass Test\n@enduml",
    #         output_dir="/tmp"
    #     )
        
    #     # Verify mock was called with correct parameters
    #     mock_generate_diagram.assert_called_once_with(
    #         diagram_type="class",
    #         code="@startuml\nclass Test\n@enduml",
    #         output_format="svg",  # Default format
    #         output_dir="/tmp"
    #     )
        
    #     # Verify result
    #     assert result == mock_generate_diagram.return_value