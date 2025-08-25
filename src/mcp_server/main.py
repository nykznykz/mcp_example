"""Main MCP server implementation using FastMCP v2.0."""

import asyncio
import logging
from typing import Any, Dict, List

from fastmcp import FastMCP
from pydantic import BaseModel

logger = logging.getLogger(__name__)

# Create the FastMCP server instance
mcp = FastMCP("Example MCP Server")


class CalculateRequest(BaseModel):
    """Request model for calculate tool."""
    expression: str


class GreetRequest(BaseModel):
    """Request model for greet tool."""
    name: str


# Define the actual functions first
def _calculate(expression: str) -> str:
    """
    Evaluate a mathematical expression safely.
    
    Args:
        expression: A mathematical expression to evaluate (e.g., "2 + 2", "10 * 5")
    
    Returns:
        The result of the calculation as a string
    """
    try:
        # Simple evaluation for basic math operations
        # In production, you'd want a more secure math parser
        allowed_chars = set("0123456789+-*/.() ")
        if not all(c in allowed_chars for c in expression):
            return f"Error: Invalid characters in expression '{expression}'"
        
        result = eval(expression)
        return f"The result of '{expression}' is {result}"
    except Exception as e:
        return f"Error calculating '{expression}': {str(e)}"


def _greet(name: str) -> str:
    """
    Generate a friendly greeting message.
    
    Args:
        name: The name of the person to greet
    
    Returns:
        A personalized greeting message
    """
    return f"Hello, {name}! Welcome to the MCP server."


# Register as MCP tools
@mcp.tool()
def calculate(expression: str) -> str:
    """
    Evaluate a mathematical expression safely.
    
    Args:
        expression: A mathematical expression to evaluate (e.g., "2 + 2", "10 * 5")
    
    Returns:
        The result of the calculation as a string
    """
    return _calculate(expression)


@mcp.tool()
def greet(name: str) -> str:
    """
    Generate a friendly greeting message.
    
    Args:
        name: The name of the person to greet
    
    Returns:
        A personalized greeting message
    """
    return _greet(name)


def _get_settings() -> Dict[str, Any]:
    """
    Get server configuration settings.
    
    Returns:
        A dictionary containing server settings
    """
    return {
        "server_name": "Example MCP Server",
        "version": "0.1.0",
        "capabilities": ["calculate", "greet"],
        "max_connections": 100,
        "timeout": 30
    }


def _get_server_info() -> Dict[str, Any]:
    """
    Get general server information.
    
    Returns:
        A dictionary containing server information
    """
    return {
        "name": "Example MCP Server",
        "description": "A sample MCP server built with FastMCP v2.0",
        "author": "MCP Developer",
        "license": "MIT"
    }


def _help_prompt() -> str:
    """
    Provide help information about available tools and resources.
    
    Returns:
        Help text describing the server's capabilities
    """
    return """
# MCP Server Help

This server provides the following capabilities:

## Tools:
- **calculate**: Evaluate mathematical expressions
  - Usage: calculate(expression="2 + 2")
  
- **greet**: Generate friendly greeting messages
  - Usage: greet(name="World")

## Resources:
- **config://settings**: Server configuration settings
- **info://server**: General server information

## Prompts:
- **help**: This help message

For more information, check the server documentation.
"""


@mcp.resource("config://settings")
def get_settings() -> Dict[str, Any]:
    """
    Get server configuration settings.
    
    Returns:
        A dictionary containing server settings
    """
    return _get_settings()


@mcp.resource("info://server")
def get_server_info() -> Dict[str, Any]:
    """
    Get general server information.
    
    Returns:
        A dictionary containing server information
    """
    return _get_server_info()


@mcp.prompt("help")
def help_prompt() -> str:
    """
    Provide help information about available tools and resources.
    
    Returns:
        Help text describing the server's capabilities
    """
    return _help_prompt()


def main() -> None:
    """Main entry point for the MCP server."""
    logging.basicConfig(level=logging.INFO)
    logger.info("Starting MCP server...")
    
    try:
        # Run the FastMCP server
        mcp.run()
    except KeyboardInterrupt:
        logger.info("Server interrupted by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
        raise


if __name__ == "__main__":
    main()