"""
Example Tool
A simple example tool for the MCP server.
"""

from typing import Dict, Any

class ExampleTool:
    """
    A simple example tool that demonstrates how to implement tools for the MCP server.
    """

    def __init__(self):
        self.name = "example_tool"
        self.description = "An example tool that echoes a message"

    def execute(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the tool with the given parameters.
        
        Args:
            parameters: A dictionary of parameters for the tool
            
        Returns:
            A dictionary containing the result
        """
        message = parameters.get("message", "No message provided")
        return {
            "echo": message,
            "timestamp": "2025-05-21T13:49:25-04:00"  # Using the provided time
        }
