# Usage Examples

This page provides examples of using UML-MCP with different environments and diagram types.

## Basic Usage with Cursor

When using Cursor with UML-MCP configured, you can generate diagrams by asking the AI assistant:

```
Generate a class diagram for a banking system with Account, Customer, and Transaction classes.
```

The AI will use UML-MCP's tools to generate and display the diagram directly in your conversation.

## AI Assistant Prompts

Here are some example prompts for generating diagrams:

### Class Diagram

```
Create a class diagram showing the relationships between the following classes:
- Person (name, age, email)
- Student (studentId, enrollCourse())
- Teacher (employeeId, teachCourse())
- Course (courseId, title, description)

Students can enroll in multiple courses, and each course can have one teacher.
```

### Sequence Diagram

```
Generate a sequence diagram for an e-commerce checkout process involving:
- Customer
- ShoppingCart
- OrderSystem
- PaymentProcessor
- InventorySystem
```

### Component Diagram

```
Create a component diagram for a microservices architecture with:
- API Gateway
- User Service
- Product Service
- Order Service
- Payment Service
- Notification Service
```

## Using MCP Tools Directly

If you're building an application that uses UML-MCP, you can call the tools directly:

### Python Example

```python
import json
import subprocess

def generate_class_diagram(code):
    # Start the MCP server process
    process = subprocess.Popen(
        ["python", "mcp_server.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Prepare MCP request
    request = {
        "type": "tool",
        "name": "generate_class_diagram",
        "args": {
            "code": code,
            "output_dir": "./output"
        }
    }
    
    # Send request to MCP server
    process.stdin.write(json.dumps(request) + "\n")
    process.stdin.flush()
    
    # Read response
    response = json.loads(process.stdout.readline())
    
    # Close process
    process.terminate()
    
    return json.loads(response["result"])

# Example usage
diagram = generate_class_diagram("""
class User {
  -name: String
  -email: String
  +register(): void
  +login(): boolean
}
""")

print(f"Diagram URL: {diagram['url']}")
print(f"Local file: {diagram['local_path']}")
```

## Integration Examples

### Web Application

```javascript
async function generateDiagram(diagramType, code) {
  const response = await fetch('/api/diagram', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      type: diagramType,
      code: code
    }),
  });
  
  const result = await response.json();
  document.getElementById('diagram').src = result.url;
  document.getElementById('playground-link').href = result.playground;
}
```

### Command Line

```bash
echo '{
  "type": "tool",
  "name": "generate_sequence_diagram",
  "args": {
    "code": "@startuml\nAlice -> Bob: Hello\nBob --> Alice: Hi\n@enduml",
    "output_dir": "./diagrams"
  }
}' | python mcp_server.py
```
