"""
Tests for the core utilities of UML-MCP.
"""
import os
import pytest
from unittest.mock import patch, MagicMock

from mcp_core.core.utils import generate_diagram
from mcp_core.core.config import MCP_SETTINGS

@pytest.fixture
def mock_kroki_client():
    """Mock the Kroki client for testing."""
    with patch('mcp_core.core.utils.kroki_client') as mock_client:
        # Setup mock response
        mock_client.generate_diagram.return_value = {
            "url": "https://kroki.io/plantuml/svg/test_url",
            "content": b"<svg>test content</svg>",
            "playground": "https://playground.example.com"
        }
        yield mock_client

def test_generate_diagram_success(mock_kroki_client, tmp_path):
    """Test successful diagram generation."""
    # Call generate_diagram with test data
    result = generate_diagram(
        diagram_type="class",
        code="@startuml\nclass Test\n@enduml",
        output_format="svg",
        output_dir=str(tmp_path)
    )
    
    # Verify result structure
    assert "code" in result
    assert "url" in result
    assert "playground" in result
    assert "local_path" in result
    
    # Verify mock was called with correct params
    mock_kroki_client.generate_diagram.assert_called_once()
    args, kwargs = mock_kroki_client.generate_diagram.call_args
    assert args[0] == "plantuml"  # Backend for class diagrams
    assert "@startuml" in args[1]  # Code contains correct markup
    assert args[2] == "svg"  # Correct output format

def test_generate_diagram_unsupported_type():
    """Test generating a diagram with unsupported type."""
    result = generate_diagram(
        diagram_type="unsupported_type",
        code="test code",
        output_format="svg"
    )
    
    # Should return error
    assert "error" in result
    assert "Unsupported diagram type" in result["error"]

def test_generate_diagram_exception(mock_kroki_client):
    """Test error handling during diagram generation."""
    # Make mock raise exception
    mock_kroki_client.generate_diagram.side_effect = Exception("Test error")
    
    # Call function and check result
    result = generate_diagram(
        diagram_type="class",
        code="@startuml\nclass Test\n@enduml",
        output_format="svg"
    )
    
    # Verify error is returned
    assert "error" in result
    assert "Test error" in result["error"]

def test_output_directory_creation(tmp_path):
    """Test that the output directory is created if it doesn't exist."""
    non_existent_dir = os.path.join(tmp_path, "new_dir")

    # Directory shouldn't exist initially
    assert not os.path.exists(non_existent_dir)

    # Call function with non-existent directory
    with patch('mcp_core.core.utils.kroki_client') as mock_client:
        mock_client.generate_diagram.return_value = {
            "url": "test_url",
            "content": b"test content",
            "playground": "test_playground"
        }
        generate_diagram(
            diagram_type="class",
            code="@startuml\nclass Test\n@enduml",
            output_format="svg",
            output_dir=non_existent_dir
        )

    # Directory should now exist
    assert os.path.exists(non_existent_dir)


def test_generate_diagram_local_plantuml(tmp_path):
    """Test diagram generation with local PlantUML client."""
    with patch('mcp_core.core.utils.USE_LOCAL_PLANTUML', True), \
         patch('mcp_core.core.utils.plantuml_client') as mock_plantuml:

        # Setup mock PlantUML client response
        output_file = os.path.join(tmp_path, "test.svg")
        mock_plantuml.generate_diagram.return_value = {
            'success': True,
            'output_path': output_file,
            'error': None
        }

        # Create mock output file
        with open(output_file, 'wb') as f:
            f.write(b"<svg>test</svg>")

        # Generate diagram
        result = generate_diagram(
            diagram_type="class",
            code="@startuml\nclass Test\n@enduml",
            output_format="svg",
            output_dir=str(tmp_path)
        )

        # Verify local PlantUML was used
        mock_plantuml.generate_diagram.assert_called_once()

        # Verify result structure
        assert "code" in result
        assert "local_path" in result
        assert "generated_by" in result
        assert result["generated_by"] == "local_plantuml"
        assert result["local_path"] == output_file


def test_generate_diagram_local_plantuml_failure_fallback(mock_kroki_client):
    """Test fallback to Kroki when local PlantUML fails."""
    with patch('mcp_core.core.utils.USE_LOCAL_PLANTUML', True), \
         patch('mcp_core.core.utils.plantuml_client') as mock_plantuml:

        # Setup mock PlantUML to fail
        mock_plantuml.generate_diagram.return_value = {
            'success': False,
            'output_path': None,
            'error': 'PlantUML execution failed'
        }

        # Generate diagram
        result = generate_diagram(
            diagram_type="class",
            code="@startuml\nclass Test\n@enduml",
            output_format="svg"
        )

        # Verify error is returned
        assert "error" in result
        assert "PlantUML generation failed" in result["error"]


def test_generate_diagram_mermaid_uses_kroki():
    """Test that Mermaid diagrams always use Kroki (not local PlantUML)."""
    with patch('mcp_core.core.utils.USE_LOCAL_PLANTUML', True), \
         patch('mcp_core.core.utils.plantuml_client') as mock_plantuml, \
         patch('mcp_core.core.utils.kroki_client') as mock_kroki:

        # Setup mock responses
        mock_kroki.generate_diagram.return_value = {
            "url": "https://kroki.io/mermaid/svg/test",
            "content": b"<svg>mermaid</svg>",
            "playground": "https://mermaid.live"
        }

        # Generate Mermaid diagram
        result = generate_diagram(
            diagram_type="mermaid",
            code="graph TD\nA-->B",
            output_format="svg"
        )

        # Verify Kroki was used, not local PlantUML
        mock_kroki.generate_diagram.assert_called_once()
        mock_plantuml.generate_diagram.assert_not_called()

        # Verify result
        assert "url" in result
        assert "mermaid" in result["url"]


def test_generate_diagram_d2_uses_kroki():
    """Test that D2 diagrams use Kroki."""
    with patch('mcp_core.core.utils.kroki_client') as mock_kroki:

        # Setup mock response
        mock_kroki.generate_diagram.return_value = {
            "url": "https://kroki.io/d2/svg/test",
            "content": b"<svg>d2</svg>",
            "playground": None
        }

        # Generate D2 diagram
        result = generate_diagram(
            diagram_type="d2",
            code="x -> y",
            output_format="svg"
        )

        # Verify Kroki was used
        mock_kroki.generate_diagram.assert_called_once()
        args, kwargs = mock_kroki.generate_diagram.call_args
        assert args[0] == "d2"  # Backend for D2 diagrams

        # Verify result
        assert "url" in result
        assert "d2" in result["url"]


def test_plantuml_code_wrapping():
    """Test that PlantUML code is wrapped with @startuml/@enduml."""
    with patch('mcp_core.core.utils.kroki_client') as mock_kroki:

        mock_kroki.generate_diagram.return_value = {
            "url": "test_url",
            "content": b"test",
            "playground": "test"
        }

        # Generate diagram without markers
        generate_diagram(
            diagram_type="class",
            code="class Test",
            output_format="svg"
        )

        # Verify code was wrapped
        call_args = mock_kroki.generate_diagram.call_args[0]
        code_arg = call_args[1]
        assert "@startuml" in code_arg
        assert "@enduml" in code_arg
        assert "class Test" in code_arg