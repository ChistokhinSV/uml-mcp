"""
Documentation generator for MCP server
"""

import json
import os
import logging
from typing import Dict, List, Any

from ..core.config import MCP_SETTINGS

logger = logging.getLogger(__name__)

# UML diagram types supported by the server
UML_TYPES = [
    "class", "sequence", "activity", "usecase", 
    "state", "component", "deployment", "object"
]

def generate_api_docs() -> Dict[str, Any]:
    """
    Generate API documentation in OpenAPI format
    
    Returns:
        Dictionary containing OpenAPI specification
    """
    logger.info("Generating API documentation")
    
    # Base OpenAPI structure
    openapi_spec = {
        "openapi": "3.0.0",
        "info": {
            "title": MCP_SETTINGS.server_name,
            "description": MCP_SETTINGS.description,
            "version": MCP_SETTINGS.version
        },
        "paths": {},
        "components": {
            "schemas": {
                "DiagramRequest": {
                    "type": "object",
                    "properties": {
                        "code": {
                            "type": "string",
                            "description": "PlantUML/Mermaid/D2 diagram code"
                        },
                        "output_dir": {
                            "type": "string",
                            "description": "Output directory path"
                        }
                    },
                    "required": ["code", "output_dir"]
                },
                "UMLDiagramRequest": {
                    "type": "object",
                    "properties": {
                        "diagram_type": {
                            "type": "string",
                            "enum": UML_TYPES,
                            "description": "Type of UML diagram"
                        },
                        "code": {
                            "type": "string",
                            "description": "PlantUML diagram code"
                        },
                        "output_dir": {
                            "type": "string",
                            "description": "Output directory path"
                        }
                    },
                    "required": ["diagram_type", "code", "output_dir"]
                },
                "DiagramResponse": {
                    "type": "object",
                    "properties": {
                        "code": {
                            "type": "string",
                            "description": "Original diagram code"
                        },
                        "url": {
                            "type": "string",
                            "description": "URL to the generated diagram"
                        },
                        "encoded": {
                            "type": "string",
                            "description": "PlantUML encoded string for the diagram"
                        },
                        "local_path": {
                            "type": "string",
                            "description": "Local file path to the saved diagram"
                        },
                        "error": {
                            "type": "string",
                            "description": "Error message if generation failed"
                        }
                    }
                }
            }
        }
    }
    
    # Add UML diagram generation tools
    for diagram_type in UML_TYPES:
        tool_name = f"generate_{diagram_type}_diagram"
        path = f"/{tool_name.replace('_', '-')}"
        
        openapi_spec["paths"][path] = {
            "post": {
                "summary": f"Generate {diagram_type} diagram",
                "description": f"Generate a UML {diagram_type} diagram using PlantUML",
                "operationId": tool_name,
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/DiagramRequest"
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Successful operation",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/DiagramResponse"
                                }
                            }
                        }
                    },
                    "400": {
                        "description": "Invalid input"
                    },
                    "500": {
                        "description": "Server error"
                    }
                }
            }
        }
    
    # Add generic UML generation endpoint
    openapi_spec["paths"]["/generate-uml"] = {
        "post": {
            "summary": "Generate any UML diagram",
            "description": "Generate a UML diagram of any supported type using PlantUML",
            "operationId": "generate_uml",
            "requestBody": {
                "required": True,
                "content": {
                    "application/json": {
                        "schema": {
                            "$ref": "#/components/schemas/UMLDiagramRequest"
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Successful operation",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/DiagramResponse"
                                }
                            }
                        }
                    },
                    "400": {
                        "description": "Invalid input"
                    },
                    "500": {
                        "description": "Server error"
                    }
                }
            }
        }
    }
    
    # Add resources
    for resource_path in ["uml://types", "uml://templates", "uml://examples", "uml://formats", "uml://server-info"]:
        path = f"/resources/{resource_path.replace('://', '-')}"
        
        openapi_spec["paths"][path] = {
            "get": {
                "summary": f"Get {resource_path}",
                "description": get_resource_description(resource_path),
                "operationId": resource_path.replace("://", "_").replace("/", "_"),
                "responses": {
                    "200": {
                        "description": "Successful operation",
                        "content": {
                            "application/json": {
                                "schema": get_resource_schema(resource_path)
                            }
                        }
                    }
                }
            }
        }
    
    logger.info("API documentation generated")
    return openapi_spec

def get_resource_description(resource_path: str) -> str:
    """Get description for a resource endpoint"""
    descriptions = {
        "uml://types": "List of supported UML diagram types and their descriptions",
        "uml://templates": "Template code for different UML diagram types",
        "uml://examples": "Example UML diagrams for reference",
        "uml://formats": "Supported output formats for diagrams",
        "uml://server-info": "Server configuration and capabilities information"
    }
    return descriptions.get(resource_path, f"Resource for {resource_path}")

def get_resource_schema(resource_path: str) -> Dict[str, Any]:
    """Get OpenAPI schema for a resource endpoint"""
    if resource_path == "uml://types":
        return {
            "type": "object",
            "properties": {
                "types": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": UML_TYPES
                    },
                    "description": "List of supported UML diagram types"
                },
                "descriptions": {
                    "type": "object",
                    "additionalProperties": {
                        "type": "string"
                    },
                    "description": "Descriptions of each diagram type"
                }
            }
        }
    elif resource_path == "uml://templates":
        return {
            "type": "object",
            "properties": {
                "templates": {
                    "type": "object",
                    "additionalProperties": {
                        "type": "string"
                    },
                    "description": "Template code for each diagram type"
                }
            }
        }
    elif resource_path == "uml://examples":
        return {
            "type": "object",
            "properties": {
                "examples": {
                    "type": "object",
                    "additionalProperties": {
                        "type": "object",
                        "properties": {
                            "code": {
                                "type": "string",
                                "description": "Example diagram code"
                            },
                            "description": {
                                "type": "string",
                                "description": "Description of the example"
                            }
                        }
                    }
                }
            }
        }
    return {"type": "object"}

def save_api_docs(output_dir: str = "docs") -> str:
    """
    Generate and save API documentation
    
    Args:
        output_dir: Directory to save the documentation
        
    Returns:
        Path to the saved documentation file
    """
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate docs
    docs = generate_api_docs()
    
    # Save as JSON
    json_path = os.path.join(output_dir, "openapi.json")
    with open(json_path, "w") as f:
        json.dump(docs, f, indent=2)
    
    logger.info(f"API documentation saved to {json_path}")
    return json_path
