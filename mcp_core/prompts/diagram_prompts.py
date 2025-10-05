"""
MCP prompts for diagram generation using the decorator pattern
"""
import logging
from typing import Dict, List, Any, Optional, Callable, TypeVar, cast

# Import FastMCP from wrapper to avoid circular imports
from mcp_core.server.fastmcp_wrapper import FastMCP
from ..core.config import MCP_SETTINGS

logger = logging.getLogger(__name__)

# Store for registered prompts when using decorator pattern
_registered_prompts: Dict[str, Dict[str, Any]] = {}

F = TypeVar('F', bound=Callable[..., Any])

def mcp_prompt(
    name: str,
    description: Optional[str] = None,
    category: str = "default"
) -> Callable[[F], F]:
    """
    Decorator for registering a function as an MCP prompt.
    
    Args:
        name: Prompt name
        description: Prompt description (defaults to function docstring if not provided)
        category: Prompt category for organization
        
    Returns:
        Decorated function
    
    Example:
        @mcp_prompt("class_diagram", description="Generate UML class diagram")
        def class_diagram_prompt(context: dict) -> str:
            # Implementation
            return prompt_text
    """
    def decorator(func: F) -> F:
        func_doc = func.__doc__ or ""
        func_description = description or func_doc.split('\n')[0] if func_doc else ""
        
        # Store prompt metadata
        _registered_prompts[name] = {
            "function": func,
            "name": name,
            "description": func_description,
            "category": category
        }
        
        # Return function unchanged
        return cast(F, func)
    
    return decorator

# Base UML diagram prompt function
@mcp_prompt("uml_diagram", description="Base prompt for UML diagram generation")
def uml_diagram_prompt(context: Dict[str, Any] = None) -> str:
    """
    Base prompt for UML diagram generation
    
    Args:
        context: Dictionary containing context information
    
    Returns:
        The prompt text
    """
    context = context or {}
    
    # Generate base prompt
    prompt = """You are an expert in UML diagrams. Create a UML diagram based on the description.
    
Follow these guidelines:
1. Use proper UML notation and syntax
2. Include all necessary elements mentioned in the description
3. Organize the diagram to be readable and clear
4. Add appropriate relationships between elements

Provide the diagram code that can be directly used to generate the UML diagram:
"""
    
    # Add diagram type specific instructions if provided in context
    if 'diagram_type' in context:
        diagram_type = context['diagram_type']
        prompt += f"\nThis should be a {diagram_type} diagram.\n"
    
    return prompt

# Class diagram prompt
@mcp_prompt("class_diagram", description="Generate UML class diagram from description")
def class_diagram_prompt(context: Dict[str, Any] = None) -> str:
    """
    Prompt for generating UML class diagrams
    
    Args:
        context: Dictionary containing context information
    
    Returns:
        The prompt text
    """
    context = context or {}
    context['diagram_type'] = 'class'
    
    # Get base prompt
    prompt = uml_diagram_prompt(context)
    
    # Add class diagram specific instructions
    prompt += """
For class diagrams, follow these additional guidelines:
1. Include class names, attributes, and methods with proper visibility (+, -, #)
2. Show inheritance using generalization relationships (empty triangle arrow)
3. Show composition using filled diamond and aggregation using empty diamond
4. Include proper multiplicities on associations (1, *, 0..1, etc.)
5. Group related classes together
6. Use interfaces where appropriate (with <<interface>> stereotype)

Example PlantUML class diagram syntax:
```
@startuml
class User {
  -name: String
  -email: String
  +login(): void
  +logout(): void
}

class Account {
  -balance: Decimal
  +deposit(amount: Decimal): void
  +withdraw(amount: Decimal): boolean
}

User "1" -- "*" Account : has >
@enduml
```

Provide the complete PlantUML code for the class diagram:
"""
    
    return prompt

# Sequence diagram prompt
@mcp_prompt("sequence_diagram", description="Generate UML sequence diagram from description")
def sequence_diagram_prompt(context: Dict[str, Any] = None) -> str:
    """
    Prompt for generating UML sequence diagrams
    
    Args:
        context: Dictionary containing context information
    
    Returns:
        The prompt text
    """
    context = context or {}
    context['diagram_type'] = 'sequence'
    
    # Get base prompt
    prompt = uml_diagram_prompt(context)
    
    # Add sequence diagram specific instructions
    prompt += """
For sequence diagrams, follow these additional guidelines:
1. Include all participants (actors, objects, systems) involved in the interaction
2. Show messages in chronological order from top to bottom
3. Include activations to show when objects are active
4. Use lifelines for all participants
5. Include return messages where appropriate
6. Add notes for clarification when needed

Example PlantUML sequence diagram syntax:
```
@startuml
actor User
participant "Web Browser" as Browser
participant "Web Server" as Server
database Database

User -> Browser: Enter credentials
activate Browser
Browser -> Server: Send login request
activate Server
Server -> Database: Validate credentials
activate Database
Database --> Server: Authentication result
deactivate Database
Server --> Browser: Login response
deactivate Server
Browser --> User: Display result
deactivate Browser
@enduml
```

Provide the complete PlantUML code for the sequence diagram:
"""
    
    return prompt

# Activity diagram prompt
@mcp_prompt("activity_diagram", description="Generate UML activity diagram from description")
def activity_diagram_prompt(context: Dict[str, Any] = None) -> str:
    """
    Prompt for generating UML activity diagrams
    
    Args:
        context: Dictionary containing context information
    
    Returns:
        The prompt text
    """
    context = context or {}
    context['diagram_type'] = 'activity'
    
    # Get base prompt
    prompt = uml_diagram_prompt(context)
    
    # Add activity diagram specific instructions
    prompt += """
For activity diagrams, follow these additional guidelines:
1. Include clear start and end points
2. Show activities as rounded rectangles
3. Use decision nodes (diamonds) for branching
4. Include merge nodes where appropriate
5. Use swimlanes if activities are performed by different actors/systems
6. Include fork and join bars for parallel activities

Example PlantUML activity diagram syntax:
```
@startuml
start
:Login to system;
if (Valid credentials?) then (yes)
  :Display dashboard;
  fork
    :Check notifications;
  fork again
    :Load user data;
  end fork
  :Display user profile;
else (no)
  :Show error message;
  :Display login form;
endif
stop
@enduml
```

Provide the complete PlantUML code for the activity diagram:
"""
    
    return prompt

# Use case diagram prompt
@mcp_prompt("usecase_diagram", description="Generate UML use case diagram from description")
def usecase_diagram_prompt(context: Dict[str, Any] = None) -> str:
    """
    Prompt for generating UML use case diagrams
    
    Args:
        context: Dictionary containing context information
    
    Returns:
        The prompt text
    """
    context = context or {}
    context['diagram_type'] = 'usecase'
    
    # Get base prompt
    prompt = uml_diagram_prompt(context)
    
    # Add use case diagram specific instructions
    prompt += """
For use case diagrams, follow these additional guidelines:
1. Include actors represented as stick figures
2. Display use cases as ovals with descriptive text
3. Show system boundary as a rectangle containing the use cases
4. Include relationships: association (line), include (dashed arrow with <<include>>), extend (dashed arrow with <<extend>>)
5. Show actor generalizations if applicable

Example PlantUML use case diagram syntax:
```
@startuml
left to right direction
actor Customer
actor Administrator

rectangle "Online Shopping System" {
  usecase "Browse Products" as UC1
  usecase "Add to Cart" as UC2
  usecase "Checkout" as UC3
  usecase "Process Payment" as UC4
  usecase "Manage Products" as UC5
  
  Customer --> UC1
  Customer --> UC2
  Customer --> UC3
  UC3 ..> UC4 : <<include>>
  Administrator --> UC5
}
@enduml
```

Provide the complete PlantUML code for the use case diagram:
"""
    
    return prompt

def register_prompts_with_server(server: FastMCP) -> List[str]:
    """
    Register all decorated prompts with the MCP server
    
    Args:
        server: The MCP server instance
        
    Returns:
        List of registered prompt names
    """
    logger.info(f"Registering {len(_registered_prompts)} prompts with the MCP server")
    
    registered_prompt_names = []
    
    for prompt_name, prompt_info in _registered_prompts.items():
        func = prompt_info["function"]
        
        # Register with server using prompt decorator
        prompt_decorator = server.prompt(prompt_name)
        prompt_decorator(func)
        
        registered_prompt_names.append(prompt_name)
        logger.debug(f"Registered prompt: {prompt_name}")
    
    return registered_prompt_names

def register_diagram_prompts(server: FastMCP) -> List[str]:
    """
    Register diagram prompts with the MCP server
    
    Args:
        server: The MCP server instance
        
    Returns:
        List of registered prompt names
    """
    logger.info("Registering diagram prompts")
    
    # Register all prompts that were decorated with @mcp_prompt
    registered_prompts = register_prompts_with_server(server)
    
    # Store registered prompts in MCP_SETTINGS
    MCP_SETTINGS.prompts = registered_prompts
    
    logger.info(f"Registered {len(registered_prompts)} diagram prompts successfully")
    logger.debug(f"Registered prompts: {registered_prompts}")
    
    return registered_prompts

def get_prompt_registry() -> Dict[str, Dict[str, Any]]:
    """
    Get the registry of all prompts registered with the decorator
    
    Returns:
        Dictionary of prompt metadata
    """
    return _registered_prompts
