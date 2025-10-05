"""
PlantUML local client with JRE detection and JAR execution support.

This module provides functionality to:
- Detect Java Runtime Environment (JRE)
- Execute plantuml.jar locally for diagram generation
- Support both PNG and SVG output formats
"""

import os
import subprocess
import logging
import shutil
from pathlib import Path
from typing import Optional, Tuple, Dict

logger = logging.getLogger(__name__)


class PlantUMLError(Exception):
    """Base exception for PlantUML errors."""
    pass


class JavaNotFoundError(PlantUMLError):
    """Java Runtime Environment not found."""
    pass


class PlantUMLJarNotFoundError(PlantUMLError):
    """plantuml.jar file not found."""
    pass


class PlantUMLClient:
    """Client for local PlantUML diagram generation using plantuml.jar.

    This client detects Java installation and uses plantuml.jar to generate
    diagrams locally without requiring a PlantUML server.

    Attributes:
        java_path: Path to the Java executable.
        jar_path: Path to the plantuml.jar file.
    """

    def __init__(self, java_path: Optional[str] = None, jar_path: Optional[str] = None):
        """
        Initialize the PlantUML client.

        Args:
            java_path: Path to Java executable. If None, will auto-detect.
            jar_path: Path to plantuml.jar. If None, will look in common locations.

        Raises:
            JavaNotFoundError: If Java is not found.
            PlantUMLJarNotFoundError: If plantuml.jar is not found.
        """
        self.java_path = java_path or self._detect_java()
        self.jar_path = jar_path or self._detect_jar()

        # Verify Java works
        self._verify_java()

        logger.info(f"PlantUML client initialized: Java={self.java_path}, JAR={self.jar_path}")

    def _detect_java(self) -> str:
        """
        Detect Java Runtime Environment installation.

        Returns:
            Path to Java executable.

        Raises:
            JavaNotFoundError: If Java is not found.
        """
        # Check environment variable first
        java_home = os.environ.get('JAVA_HOME')
        if java_home:
            java_exe = os.path.join(java_home, 'bin', 'java')
            if os.path.isfile(java_exe):
                return java_exe

        # Try to find java in PATH
        java_path = shutil.which('java')
        if java_path:
            return java_path

        # Common Java installation locations (Windows)
        if os.name == 'nt':
            common_paths = [
                r"C:\Program Files\Java",
                r"C:\Program Files (x86)\Java",
                r"C:\Program Files\Eclipse Adoptium",
                r"C:\Program Files\Microsoft\jdk",
            ]

            for base_path in common_paths:
                if os.path.isdir(base_path):
                    # Find any JRE/JDK directory
                    for item in os.listdir(base_path):
                        java_exe = os.path.join(base_path, item, 'bin', 'java.exe')
                        if os.path.isfile(java_exe):
                            return java_exe

        raise JavaNotFoundError(
            "Java Runtime Environment not found. Please install Java 11+ or set JAVA_HOME environment variable.\n"
            "Download from: https://adoptium.net/ or https://www.oracle.com/java/technologies/downloads/"
        )

    def _detect_jar(self) -> str:
        """
        Detect plantuml.jar file location.

        Returns:
            Path to plantuml.jar file.

        Raises:
            PlantUMLJarNotFoundError: If plantuml.jar is not found.
        """
        # Check environment variable
        jar_env = os.environ.get('PLANTUML_JAR_PATH')
        if jar_env and os.path.isfile(jar_env):
            return jar_env

        # Common locations to check
        script_dir = Path(__file__).parent.parent
        common_paths = [
            script_dir / 'extension' / 'bin' / 'plantuml.jar',
            script_dir / 'bin' / 'plantuml.jar',
            script_dir / 'plantuml.jar',
            Path.home() / '.plantuml' / 'plantuml.jar',
            Path('/usr/local/bin/plantuml.jar'),
            Path('/opt/plantuml/plantuml.jar'),
        ]

        for jar_path in common_paths:
            if jar_path.is_file():
                return str(jar_path)

        raise PlantUMLJarNotFoundError(
            f"plantuml.jar not found. Checked locations:\n" +
            "\n".join(f"  - {p}" for p in common_paths) +
            "\n\nDownload from: https://github.com/plantuml/plantuml/releases/latest"
        )

    def _verify_java(self):
        """
        Verify Java installation works.

        Raises:
            JavaNotFoundError: If Java verification fails.
        """
        try:
            result = subprocess.run(
                [self.java_path, '-version'],
                capture_output=True,
                text=True,
                timeout=10
            )

            # Java writes version to stderr
            version_output = result.stderr or result.stdout
            logger.debug(f"Java version: {version_output.strip()}")

        except (subprocess.SubprocessError, OSError) as e:
            raise JavaNotFoundError(f"Failed to execute Java: {e}")

    def get_java_version(self) -> str:
        """
        Get Java version information.

        Returns:
            Java version string.
        """
        try:
            result = subprocess.run(
                [self.java_path, '-version'],
                capture_output=True,
                text=True,
                timeout=10
            )
            version_output = result.stderr or result.stdout
            return version_output.strip()
        except Exception as e:
            return f"Unknown (error: {e})"

    def generate_diagram(
        self,
        diagram_code: str,
        output_format: str = 'svg',
        output_file: Optional[str] = None
    ) -> Dict[str, any]:
        """
        Generate a diagram using plantuml.jar.

        Args:
            diagram_code: PlantUML diagram source code.
            output_format: Output format (svg, png, txt).
            output_file: Optional output file path. If None, creates temp file.

        Returns:
            Dictionary containing:
            - success: Boolean indicating success
            - output_path: Path to generated diagram file
            - error: Error message if any

        Raises:
            PlantUMLError: If diagram generation fails.
        """
        import tempfile

        # Validate output format
        supported_formats = ['svg', 'png', 'txt', 'eps', 'pdf']
        if output_format not in supported_formats:
            raise PlantUMLError(
                f"Unsupported output format '{output_format}'. "
                f"Supported: {', '.join(supported_formats)}"
            )

        # Create temp input file
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.puml',
            delete=False,
            encoding='utf-8'
        ) as tmp_input:
            tmp_input.write(diagram_code)
            input_path = tmp_input.name

        try:
            # Determine output path
            if output_file:
                output_dir = os.path.dirname(output_file) or '.'
                output_filename = os.path.basename(output_file)
            else:
                output_dir = tempfile.gettempdir()
                output_filename = None

            # Build command
            # Format flags: -tsvg, -tpng, -ttxt, etc.
            cmd = [
                self.java_path,
                '-jar',
                self.jar_path,
                f'-t{output_format}',
                '-charset', 'UTF-8',
                '-o', output_dir,
                input_path
            ]

            logger.debug(f"Running PlantUML: {' '.join(cmd)}")

            # Execute PlantUML
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode != 0:
                error_msg = result.stderr or result.stdout or "Unknown error"
                logger.error(f"PlantUML generation failed: {error_msg}")
                return {
                    'success': False,
                    'output_path': None,
                    'error': error_msg
                }

            # Find generated file
            input_basename = os.path.splitext(os.path.basename(input_path))[0]
            generated_file = os.path.join(output_dir, f"{input_basename}.{output_format}")

            # Rename if custom output filename specified
            if output_file and os.path.isfile(generated_file):
                final_path = os.path.join(output_dir, output_filename)
                if generated_file != final_path:
                    os.replace(generated_file, final_path)
                    generated_file = final_path

            if not os.path.isfile(generated_file):
                return {
                    'success': False,
                    'output_path': None,
                    'error': f"Generated file not found at {generated_file}"
                }

            logger.info(f"Diagram generated successfully: {generated_file}")

            return {
                'success': True,
                'output_path': generated_file,
                'error': None
            }

        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'output_path': None,
                'error': "PlantUML execution timed out (60s limit)"
            }
        except Exception as e:
            logger.error(f"PlantUML execution error: {e}")
            return {
                'success': False,
                'output_path': None,
                'error': str(e)
            }
        finally:
            # Clean up temp input file
            try:
                os.unlink(input_path)
            except Exception:
                pass


def check_java_installation() -> Tuple[bool, str]:
    """
    Check if Java is installed and accessible.

    Returns:
        Tuple of (is_installed, version_or_error_message).
    """
    try:
        client = PlantUMLClient()
        version = client.get_java_version()
        return True, version
    except JavaNotFoundError as e:
        return False, str(e)
    except Exception as e:
        return False, f"Error checking Java: {e}"


def check_plantuml_jar() -> Tuple[bool, str]:
    """
    Check if plantuml.jar is available.

    Returns:
        Tuple of (is_available, path_or_error_message).
    """
    try:
        client = PlantUMLClient()
        return True, client.jar_path
    except PlantUMLJarNotFoundError as e:
        return False, str(e)
    except Exception as e:
        return False, f"Error checking plantuml.jar: {e}"
