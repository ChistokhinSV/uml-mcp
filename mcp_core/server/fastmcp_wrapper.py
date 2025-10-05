"""
Wrapper for FastMCP server to ensure compatibility
"""

import logging
import sys
import json
import os
from typing import Any, Callable, Dict, List, Optional, Union

logger = logging.getLogger(__name__)

# Determine if we should use the mock implementation
use_mock = False

# Check if we're in a development or test environment
is_dev_or_test = (
    os.environ.get("TESTING", "false").lower() in ("true", "1", "yes") or
    os.environ.get("DEVELOPMENT", "false").lower() in ("true", "1", "yes") or
    "pytest" in sys.modules or
    os.environ.get("MOCK_FASTMCP", "false").lower() in ("true", "1", "yes")
)

if is_dev_or_test:
    use_mock = True
    logger.warning("Using mock FastMCP implementation for development/testing")
else:
    try:
        import fastmcp
        if not hasattr(fastmcp, 'FastMCP'):
            raise ImportError("FastMCP class not found in fastmcp package")
        logger.info("Using production FastMCP implementation")
        from fastmcp import FastMCP, Context
    except ImportError as e:
        logger.error(f"FastMCP package error: {str(e)}")
        raise ImportError("FastMCP package is required but not installed. Set MOCK_FASTMCP=true to use mock implementation.")

# Define mock classes if needed
if use_mock:
    class Context:
        def __init__(self):
            self.data = {}
            
        def get(self, key: str, default: Any = None) -> Any:
            return self.data.get(key, default)
            
        def set(self, key: str, value: Any):
            self.data[key] = value

    class FastMCP:
        def __init__(self, name: str):
            self.name = name
            self._tools = {}
            self._prompts = {}
            self._resources = {}
            self.logger = logging.getLogger(__name__)

        def tool(self, *args, **kwargs):
            def decorator(func: Callable) -> Callable:
                tool_name = kwargs.get('name', func.__name__)
                self._tools[tool_name] = func
                return func
            return decorator

        def prompt(self, prompt_name: str = None):
            def decorator(func: Callable) -> Callable:
                name = prompt_name or func.__name__
                self._prompts[name] = func
                return func
            return decorator

        def resource(self, path: str):
            def decorator(func: Callable) -> Callable:
                self._resources[path] = func
                return func
            return decorator

        def run(self, transport: str = 'stdio', host: str = None, port: int = None):
            if transport == 'stdio':
                self._run_stdio()
            elif transport == 'http':
                self._run_http(host, port)
            else:
                raise ValueError(f"Unsupported transport: {transport}")

        def _run_stdio(self):
            """Run the server in stdio mode"""
            self.logger.info(f"Starting {self.name} in stdio mode")
            while True:
                try:
                    line = input()
                    if not line:
                        continue
                    request = json.loads(line)
                    response = self._handle_request(request)
                    print(json.dumps(response))
                except EOFError:
                    break
                except Exception as e:
                    self.logger.error(f"Error handling request: {e}")
                    response = {"error": str(e)}
                    print(json.dumps(response))

        def _run_http(self, host: str, port: int):
            self.logger.info(f"Starting {self.name} HTTP server on {host}:{port}")
            # Mock HTTP server implementation
            pass

        def _handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
            """Handle an MCP request and return the response."""
            try:
                if 'type' not in request:
                    raise ValueError("Missing request type")

                if request['type'] == 'tool':
                    tool_name = request.get('tool')
                    if tool_name not in self._tools:
                        raise ValueError(f"Unknown tool: {tool_name}")
                    tool = self._tools[tool_name]
                    args = request.get('args', {})
                    result = tool(**args)
                    return {"result": result}
                    
                elif request['type'] == 'prompt':
                    prompt_name = request.get('prompt')
                    if prompt_name not in self._prompts:
                        raise ValueError(f"Unknown prompt: {prompt_name}")
                    prompt = self._prompts[prompt_name]
                    args = request.get('args', {})
                    result = prompt(**args)
                    return {"result": result}
                    
                elif request['type'] == 'resource':
                    path = request.get('path')
                    if path not in self._resources:
                        raise ValueError(f"Unknown resource: {path}")
                    resource = self._resources[path]
                    result = resource()
                    return {"result": result}
                    
                else:
                    raise ValueError(f"Unknown request type: {request['type']}")
                    
            except Exception as e:
                return {"error": str(e)}

# Export the required classes
__all__ = ["FastMCP", "Context"]