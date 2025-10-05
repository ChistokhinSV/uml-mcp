"""
Tests for the PlantUML local client.
"""
import os
import pytest
import tempfile
from unittest.mock import patch, MagicMock, mock_open
from pathlib import Path

from plantuml_local import (
    PlantUMLClient,
    PlantUMLError,
    JavaNotFoundError,
    PlantUMLJarNotFoundError,
    check_java_installation,
    check_plantuml_jar,
)


@pytest.fixture
def mock_java_found():
    """Mock Java installation detection."""
    with patch('shutil.which', return_value='/usr/bin/java'):
        yield


@pytest.fixture
def mock_java_not_found():
    """Mock Java not found."""
    with patch('shutil.which', return_value=None), \
         patch.dict(os.environ, {}, clear=True):
        yield


@pytest.fixture
def mock_jar_found(tmp_path):
    """Mock plantuml.jar found."""
    jar_path = tmp_path / "plantuml.jar"
    jar_path.write_bytes(b"fake jar content")

    with patch.dict(os.environ, {'PLANTUML_JAR_PATH': str(jar_path)}):
        yield str(jar_path)


@pytest.fixture
def mock_jar_not_found():
    """Mock plantuml.jar not found."""
    with patch.dict(os.environ, {}, clear=True), \
         patch('pathlib.Path.is_file', return_value=False):
        yield


class TestPlantUMLClient:
    """Test suite for PlantUMLClient."""

    def test_initialization_success(self, mock_java_found, mock_jar_found):
        """Test successful client initialization."""
        with patch.object(PlantUMLClient, '_verify_java'):
            client = PlantUMLClient()
            assert client.java_path is not None
            assert client.jar_path is not None

    def test_initialization_java_not_found(self, mock_jar_found):
        """Test initialization fails when Java not found."""
        with patch('shutil.which', return_value=None), \
             patch.dict(os.environ, {}, clear=True), \
             patch('os.path.isfile', return_value=False), \
             patch('os.name', 'posix'):  # Force non-Windows to avoid Windows-specific paths
            with pytest.raises(JavaNotFoundError):
                PlantUMLClient()

    def test_initialization_jar_not_found(self, mock_java_found, tmp_path):
        """Test initialization fails when JAR not found."""
        # Mock Path.home() to return temp directory to avoid home dir resolution issues
        with patch.object(PlantUMLClient, '_verify_java'), \
             patch.dict(os.environ, {}, clear=True), \
             patch('pathlib.Path.home', return_value=tmp_path), \
             patch('pathlib.Path.is_file', return_value=False):
            with pytest.raises(PlantUMLJarNotFoundError):
                PlantUMLClient()

    def test_custom_java_path(self, mock_jar_found):
        """Test initialization with custom Java path."""
        custom_java = "/custom/path/java"
        with patch.object(PlantUMLClient, '_verify_java'):
            client = PlantUMLClient(java_path=custom_java)
            assert client.java_path == custom_java

    def test_custom_jar_path(self, mock_java_found):
        """Test initialization with custom JAR path."""
        custom_jar = "/custom/path/plantuml.jar"
        with patch.object(PlantUMLClient, '_verify_java'):
            client = PlantUMLClient(jar_path=custom_jar)
            assert client.jar_path == custom_jar

    @patch('subprocess.run')
    def test_verify_java_success(self, mock_run, mock_java_found, mock_jar_found):
        """Test Java verification succeeds."""
        mock_run.return_value = MagicMock(
            returncode=0,
            stderr="openjdk version \"21.0.1\"\n",
            stdout=""
        )

        client = PlantUMLClient()
        # Should not raise exception
        assert client is not None

    @patch('subprocess.run')
    def test_verify_java_failure(self, mock_run, mock_java_found, mock_jar_found):
        """Test Java verification fails."""
        mock_run.side_effect = OSError("Java not executable")

        with pytest.raises(JavaNotFoundError, match="Failed to execute Java"):
            PlantUMLClient()

    @patch('subprocess.run')
    def test_get_java_version(self, mock_run, mock_java_found, mock_jar_found):
        """Test getting Java version."""
        mock_run.return_value = MagicMock(
            returncode=0,
            stderr="openjdk version \"21.0.1\"\n",
            stdout=""
        )

        client = PlantUMLClient()
        version = client.get_java_version()
        assert "21.0.1" in version

    @patch('subprocess.run')
    def test_generate_diagram_success(self, mock_run, mock_java_found, mock_jar_found, tmp_path):
        """Test successful diagram generation."""
        # Mock Java verification
        mock_run.return_value = MagicMock(returncode=0, stderr="java version", stdout="")
        client = PlantUMLClient()

        # Mock PlantUML execution
        diagram_code = "@startuml\nclass Test\n@enduml"
        output_file = tmp_path / "test.svg"

        # Create the expected output file that PlantUML would create
        with patch('tempfile.NamedTemporaryFile') as mock_temp:
            temp_file = MagicMock()
            temp_file.name = str(tmp_path / "test.puml")
            temp_file.__enter__ = MagicMock(return_value=temp_file)
            temp_file.__exit__ = MagicMock(return_value=False)
            mock_temp.return_value = temp_file

            # Mock successful PlantUML execution
            def run_side_effect(*args, **kwargs):
                # Create the output file that PlantUML would generate
                generated_file = tmp_path / "test.svg"
                generated_file.write_text("<svg>test</svg>")
                return MagicMock(returncode=0, stdout="", stderr="")

            mock_run.side_effect = run_side_effect

            result = client.generate_diagram(
                diagram_code=diagram_code,
                output_format='svg',
                output_file=str(output_file)
            )

            assert result['success'] is True
            assert result['output_path'] is not None
            assert result['error'] is None

    @patch('subprocess.run')
    def test_generate_diagram_unsupported_format(self, mock_run, mock_java_found, mock_jar_found):
        """Test diagram generation with unsupported format."""
        mock_run.return_value = MagicMock(returncode=0, stderr="java version", stdout="")
        client = PlantUMLClient()

        with pytest.raises(PlantUMLError, match="Unsupported output format"):
            client.generate_diagram(
                diagram_code="@startuml\nclass Test\n@enduml",
                output_format='unsupported'
            )

    @patch('subprocess.run')
    def test_generate_diagram_execution_failure(self, mock_run, mock_java_found, mock_jar_found):
        """Test diagram generation when PlantUML execution fails."""
        # First call for Java verification
        # Subsequent calls for PlantUML execution
        mock_run.side_effect = [
            MagicMock(returncode=0, stderr="java version", stdout=""),  # verify_java
            MagicMock(returncode=1, stderr="PlantUML error", stdout="")  # generate_diagram
        ]

        client = PlantUMLClient()

        with patch('tempfile.NamedTemporaryFile') as mock_temp:
            temp_file = MagicMock()
            temp_file.name = "/tmp/test.puml"
            temp_file.__enter__ = MagicMock(return_value=temp_file)
            temp_file.__exit__ = MagicMock(return_value=False)
            mock_temp.return_value = temp_file

            result = client.generate_diagram(
                diagram_code="@startuml\nclass Test\n@enduml",
                output_format='svg'
            )

            assert result['success'] is False
            assert result['error'] is not None

    @patch('subprocess.run')
    def test_generate_diagram_timeout(self, mock_run, mock_java_found, mock_jar_found):
        """Test diagram generation timeout."""
        import subprocess

        mock_run.side_effect = [
            MagicMock(returncode=0, stderr="java version", stdout=""),  # verify_java
            subprocess.TimeoutExpired(cmd="java", timeout=60)  # generate_diagram
        ]

        client = PlantUMLClient()

        with patch('tempfile.NamedTemporaryFile') as mock_temp:
            temp_file = MagicMock()
            temp_file.name = "/tmp/test.puml"
            temp_file.__enter__ = MagicMock(return_value=temp_file)
            temp_file.__exit__ = MagicMock(return_value=False)
            mock_temp.return_value = temp_file

            result = client.generate_diagram(
                diagram_code="@startuml\nclass Test\n@enduml",
                output_format='svg'
            )

            assert result['success'] is False
            assert "timed out" in result['error']


class TestHelperFunctions:
    """Test helper functions."""

    @patch('plantuml_local.plantuml_client.PlantUMLClient')
    def test_check_java_installation_success(self, mock_client):
        """Test Java installation check success."""
        mock_instance = MagicMock()
        mock_instance.get_java_version.return_value = "openjdk version \"21.0.1\""
        mock_client.return_value = mock_instance

        is_installed, message = check_java_installation()
        assert is_installed is True
        assert "21.0.1" in message

    @patch('plantuml_local.plantuml_client.PlantUMLClient')
    def test_check_java_installation_failure(self, mock_client):
        """Test Java installation check failure."""
        mock_client.side_effect = JavaNotFoundError("Java not found")

        is_installed, message = check_java_installation()
        assert is_installed is False
        assert "Java not found" in message

    @patch('plantuml_local.plantuml_client.PlantUMLClient')
    def test_check_plantuml_jar_success(self, mock_client):
        """Test PlantUML JAR check success."""
        mock_instance = MagicMock()
        mock_instance.jar_path = "/path/to/plantuml.jar"
        mock_client.return_value = mock_instance

        is_available, message = check_plantuml_jar()
        assert is_available is True
        assert "/path/to/plantuml.jar" in message

    @patch('plantuml_local.plantuml_client.PlantUMLClient')
    def test_check_plantuml_jar_failure(self, mock_client):
        """Test PlantUML JAR check failure."""
        mock_client.side_effect = PlantUMLJarNotFoundError("JAR not found")

        is_available, message = check_plantuml_jar()
        assert is_available is False
        assert "JAR not found" in message


class TestJavaDetection:
    """Test Java detection logic."""

    def test_detect_java_from_path(self):
        """Test Java detection from PATH."""
        with patch('shutil.which', return_value='/usr/bin/java'), \
             patch('plantuml_local.plantuml_client.PlantUMLClient._detect_jar', return_value='/fake/jar'), \
             patch('plantuml_local.plantuml_client.PlantUMLClient._verify_java'):
            client = PlantUMLClient()
            assert '/usr/bin/java' in client.java_path

    def test_detect_java_from_java_home(self):
        """Test Java detection from JAVA_HOME."""
        java_home = "/opt/java"
        java_exe = os.path.join(java_home, 'bin', 'java')

        with patch.dict(os.environ, {'JAVA_HOME': java_home}), \
             patch('os.path.isfile', return_value=True), \
             patch('plantuml_local.plantuml_client.PlantUMLClient._detect_jar', return_value='/fake/jar'), \
             patch('plantuml_local.plantuml_client.PlantUMLClient._verify_java'):
            client = PlantUMLClient()
            assert java_exe == client.java_path


class TestJarDetection:
    """Test PlantUML JAR detection logic."""

    def test_detect_jar_from_env(self, tmp_path):
        """Test JAR detection from environment variable."""
        jar_path = tmp_path / "plantuml.jar"
        jar_path.write_bytes(b"fake")

        with patch.dict(os.environ, {'PLANTUML_JAR_PATH': str(jar_path)}), \
             patch('plantuml_local.plantuml_client.PlantUMLClient._detect_java', return_value='/usr/bin/java'), \
             patch('plantuml_local.plantuml_client.PlantUMLClient._verify_java'):
            client = PlantUMLClient()
            assert client.jar_path == str(jar_path)

    def test_detect_jar_from_extension_bin(self, tmp_path):
        """Test JAR detection from extension/bin directory."""
        # This test verifies that the actual code can find the jar in extension/bin
        # We use the real project structure
        import plantuml_local.plantuml_client as pc

        script_dir = Path(pc.__file__).parent.parent
        expected_jar = script_dir / 'extension' / 'bin' / 'plantuml.jar'

        # Skip if jar doesn't exist in the real project
        if not expected_jar.is_file():
            pytest.skip("plantuml.jar not found in extension/bin")

        with patch('plantuml_local.plantuml_client.PlantUMLClient._detect_java', return_value='/usr/bin/java'), \
             patch('plantuml_local.plantuml_client.PlantUMLClient._verify_java'), \
             patch('pathlib.Path.home', return_value=tmp_path), \
             patch.dict(os.environ, {}, clear=True):  # Clear env to test auto-detection

            client = PlantUMLClient()
            assert str(expected_jar) == client.jar_path
