# Claude Desktop Integration

This guide explains how to integrate UML-MCP with Claude Desktop for generating diagrams directly in your conversations.

## Overview

Claude Desktop can connect to the UML-MCP server through the Model Context Protocol (MCP), allowing you to generate and visualize UML diagrams and other supported diagram types within your Claude conversations.

## Setup Instructions

### 1. Install and Configure UML-MCP

Make sure you have the UML-MCP server properly installed and configured on your system. See the [Installation](../installation.md) guide for details.

### 2. Claude Desktop Configuration

Claude Desktop requires specific configuration to connect to the UML-MCP server:

1. Open Claude Desktop
2. Go to Settings (gear icon) → Advanced → MCP Servers
3. Add a new MCP server with the following details:
   - **Name**: UML-MCP-Server
   - **Command**: python (or the full path to your Python executable)
   - **Arguments**: `/path/to/uml-mcp/mcp_server.py` (replace with actual path)
   - **Working Directory**: `/path/to/uml-mcp` (replace with actual path)
   - **Output Directory**: Directory where you want diagrams to be saved

Example configuration:
```json
{
  "mcpServers": {
    "UML-MCP-Server": {
      "command": "python",
      "args": ["/path/to/uml-mcp/mcp_server.py"],
      "cwd": "/path/to/uml-mcp",
      "output_dir": "/path/to/output"
    }
  }
}
```

### 3. Test the Integration

1. Restart Claude Desktop after saving the configuration
2. In a new conversation, ask Claude to create a UML diagram
3. Claude should be able to generate the diagram using the UML-MCP server

Example prompt:
```
Create a UML class diagram for a simple e-commerce system with Customer, Product, and Order classes.
```

## Troubleshooting

### Server Connection Issues

If Claude Desktop cannot connect to the UML-MCP server:

1. Verify the server is running by launching it manually first
2. Check paths in your configuration are correct and absolute
3. Ensure you have the required permissions for the directories
4. Check Claude Desktop logs for connection errors

### Diagram Generation Problems

If diagrams aren't being generated correctly:

1. Verify the UML-MCP server is running without errors
2. Check the output directory permissions
3. Try generating different diagram types to isolate the issue
4. Verify that all required dependencies are installed

## Advanced Configuration

### Custom Templates

You can customize how diagrams appear in Claude Desktop by modifying the templates in the UML-MCP server. See [Advanced Configuration](../configuration.md#custom-templates) for details.

### Output Formats

Claude Desktop works best with SVG and PNG formats. You can specify the preferred format in your prompts to Claude or configure defaults in the UML-MCP server.

## Related Resources

- [Configuration Options](../configuration.md)
- [UML Diagram Examples](../examples.md)
- [Supported Diagram Types](../diagrams/uml.md)