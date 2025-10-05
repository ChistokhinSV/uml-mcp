"""
Utility functions for MCP server
"""

import os
import logging
import datetime
import json
from typing import Dict, Any, Optional
import base64
import zlib

from kroki.kroki import Kroki
from .config import MCP_SETTINGS

# Import PlantUML client for local generation
try:
    from plantuml import PlantUMLClient, JavaNotFoundError, PlantUMLJarNotFoundError
    PLANTUML_AVAILABLE = True
except ImportError:
    PLANTUML_AVAILABLE = False
    PlantUMLClient = None
    JavaNotFoundError = None
    PlantUMLJarNotFoundError = None

# Configure logging
def setup_logging():
    """Configure and setup logging"""
    # Create logs directory
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    
    # Generate log filename with date
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    log_file = os.path.join(log_dir, f"uml_mcp_server_{current_date}.log")
    
    # Configure root logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # Create file handler
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    logging.info("Logging system initialized")
    return logger

# Initialize Kroki client with server from configuration
kroki_client = Kroki(base_url=MCP_SETTINGS.kroki_server)

# Initialize PlantUML client if local PlantUML is enabled
plantuml_client = None
USE_LOCAL_PLANTUML = os.environ.get("USE_LOCAL_PLANTUML", "false").lower() == "true"

if USE_LOCAL_PLANTUML and PLANTUML_AVAILABLE:
    try:
        java_path = os.environ.get("JAVA_PATH")
        jar_path = os.environ.get("PLANTUML_JAR_PATH")
        plantuml_client = PlantUMLClient(java_path=java_path, jar_path=jar_path)
        logging.info(f"Local PlantUML client initialized: {plantuml_client.jar_path}")
    except (JavaNotFoundError, PlantUMLJarNotFoundError) as e:
        logging.warning(f"Failed to initialize PlantUML client: {e}. Falling back to Kroki.")
        USE_LOCAL_PLANTUML = False
    except Exception as e:
        logging.warning(f"Unexpected error initializing PlantUML client: {e}. Falling back to Kroki.")
        USE_LOCAL_PLANTUML = False

def generate_diagram(diagram_type: str, code: str, output_format: str = "png", output_dir: Optional[str] = None) -> Dict[str, Any]:
    """
    Generate a diagram using the appropriate service (Kroki, PlantUML, etc.)
    
    Args:
        diagram_type: Type of diagram (class, sequence, mermaid, d2, etc.)
        code: The diagram code/description
        output_format: Output format (png, svg, etc.)
        output_dir: Directory to save the generated image
        
    Returns:
        Dict containing code, URL, and local file path
    """
    logger = logging.getLogger(__name__)
    logger.info(f"Generating {diagram_type} diagram")
    
    # Get the output directory (use default if not provided)
    if output_dir is None:
        output_dir = MCP_SETTINGS.output_dir
    
    # Ensure output directory exists
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        logger.debug(f"Using output directory: {output_dir}")
    
    # Get diagram configuration
    diagram_config = MCP_SETTINGS.diagram_types.get(diagram_type.lower())
    if not diagram_config:
        error_msg = f"Unsupported diagram type: {diagram_type}"
        logger.error(error_msg)
        return {
            "code": code,
            "error": error_msg
        }
    
    # Determine which backend service to use
    backend_type = diagram_config.backend
    
    # Handle different diagram types
    try:
        # Create filename prefix
        filename_prefix = f"{diagram_type}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Prepare code based on backend type
        if backend_type == "plantuml":
            # Ensure PlantUML markup is present
            if "@startuml" not in code:
                code = f"@startuml\n{code}"
            if "@enduml" not in code:
                code = f"{code}\n@enduml"

        # Choose generation method based on backend and configuration
        local_path = None

        # Use local PlantUML client if enabled and backend is plantuml
        if USE_LOCAL_PLANTUML and plantuml_client and backend_type == "plantuml":
            logger.info("Using local PlantUML client for diagram generation")

            # Generate output filename if output_dir is provided
            if output_dir:
                local_path = os.path.join(output_dir, f"{filename_prefix}.{output_format}")

            # Generate diagram locally
            result_local = plantuml_client.generate_diagram(
                diagram_code=code,
                output_format=output_format,
                output_file=local_path
            )

            if not result_local['success']:
                error_msg = result_local.get('error', 'Unknown error')
                logger.error(f"Local PlantUML generation failed: {error_msg}")
                return {
                    "code": code,
                    "url": None,
                    "playground": None,
                    "local_path": None,
                    "error": f"PlantUML generation failed: {error_msg}"
                }

            # Read generated file content for Kroki URL generation
            local_path = result_local['output_path']

            # Generate Kroki URL for playground (optional)
            try:
                kroki_url = kroki_client.get_url(backend_type, code, output_format)
                playground = kroki_client.get_playground_url(backend_type, code)
            except Exception:
                kroki_url = None
                playground = None

            return {
                "code": code,
                "url": kroki_url,
                "playground": playground,
                "local_path": local_path,
                "generated_by": "local_plantuml"
            }

        else:
            # Use Kroki service for generation
            logger.info("Using Kroki service for diagram generation")
            result = kroki_client.generate_diagram(backend_type, code, output_format)

            # If output directory is provided, save the image locally
            if output_dir:
                local_path = os.path.join(output_dir, f"{filename_prefix}.{output_format}")
                with open(local_path, 'wb') as f:
                    f.write(result["content"])
                logger.info(f"Diagram saved to {local_path}")
        
        return {
            "code": code,
            "url": result["url"],
            "playground": result.get("playground"),
            "local_path": local_path
        }
    
    except Exception as e:
        logger.error(f"Error generating diagram: {str(e)}")
        # Return partial result if possible
        return {
            "code": code,
            "url": None,
            "playground": None,
            "local_path": None,
            "error": str(e)
        }

# Initialize logger
logger = setup_logging()
