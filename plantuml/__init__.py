"""
PlantUML local client package.

Provides local PlantUML diagram generation using plantuml.jar.
"""

from .plantuml_client import (
    PlantUMLClient,
    PlantUMLError,
    JavaNotFoundError,
    PlantUMLJarNotFoundError,
    check_java_installation,
    check_plantuml_jar,
)

__all__ = [
    'PlantUMLClient',
    'PlantUMLError',
    'JavaNotFoundError',
    'PlantUMLJarNotFoundError',
    'check_java_installation',
    'check_plantuml_jar',
]
