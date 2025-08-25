"""Integration tests for the MCP server."""

import pytest
from unittest.mock import Mock, patch
import json

from mcp_server.main import mcp, _calculate as calculate, _greet as greet, _get_settings as get_settings, _get_server_info as get_server_info, _help_prompt as help_prompt


class TestMCPIntegration:
    """Integration tests for the MCP server."""
    
    def test_server_initialization(self):
        """Test that the MCP server initializes correctly."""
        assert mcp is not None
        assert hasattr(mcp, 'tool')
        assert hasattr(mcp, 'resource')
        assert hasattr(mcp, 'prompt')
    
    def test_tools_registration(self):
        """Test that tools are properly registered."""
        # Note: This test depends on the actual FastMCP implementation
        # In a real scenario, you'd test the actual tool registry
        assert callable(calculate)
        assert callable(greet)
    
    def test_calculate_tool_integration(self):
        """Test calculate tool in integration context."""
        # Test various calculations
        test_cases = [
            ("1 + 1", "2"),
            ("10 * 2", "20"),
            ("100 / 10", "10"),
            ("15 - 5", "10"),
        ]
        
        for expression, expected in test_cases:
            result = calculate(expression)
            assert expected in result
            assert "The result of" in result
    
    def test_greet_tool_integration(self):
        """Test greet tool in integration context."""
        test_names = ["Alice", "Bob", "Charlie", "世界"]
        
        for name in test_names:
            result = greet(name)
            assert f"Hello, {name}!" in result
            assert "Welcome to the MCP server" in result
    
    def test_error_handling_integration(self):
        """Test error handling in integration context."""
        # Test invalid calculations
        invalid_expressions = [
            "invalid_expression",
            "1 / 0",
            "import sys",
            "",
        ]
        
        for expression in invalid_expressions:
            result = calculate(expression)
            assert "Error" in result
    
    @patch('mcp_server.main.logger')
    def test_logging_integration(self, mock_logger):
        """Test logging integration."""
        # This would test actual logging calls in a real server context
        # For now, we just verify the logger exists and can be mocked
        assert mock_logger is not None


class TestServerEndToEnd:
    """End-to-end tests simulating full server interactions."""
    
    def setup_method(self):
        """Set up test method."""
        self.mock_client = Mock()
    
    def test_full_workflow_calculate(self):
        """Test full workflow for calculation requests."""
        # Simulate a client request for calculation
        expression = "2 + 3 * 4"
        
        # Process the request
        result = calculate(expression)
        
        # Verify the result
        assert "The result of '2 + 3 * 4' is 14" == result
    
    def test_full_workflow_greet(self):
        """Test full workflow for greeting requests."""
        # Simulate a client request for greeting
        name = "Integration Test"
        
        # Process the request
        result = greet(name)
        
        # Verify the result
        expected = "Hello, Integration Test! Welcome to the MCP server."
        assert result == expected
    
    def test_multiple_requests_sequence(self):
        """Test handling multiple requests in sequence."""
        # Simulate multiple requests
        requests = [
            ("calculate", "5 + 5"),
            ("greet", "User1"),
            ("calculate", "10 * 2"),
            ("greet", "User2"),
        ]
        
        results = []
        for request_type, param in requests:
            if request_type == "calculate":
                result = calculate(param)
            elif request_type == "greet":
                result = greet(param)
            results.append(result)
        
        # Verify all results
        assert len(results) == 4
        assert "The result of '5 + 5' is 10" == results[0]
        assert "Hello, User1!" in results[1]
        assert "The result of '10 * 2' is 20" == results[2]
        assert "Hello, User2!" in results[3]


class TestServerResources:
    """Test server resource endpoints."""
    
    def test_settings_resource(self):
        """Test the settings resource."""        
        settings = get_settings()
        
        # Verify settings structure
        assert isinstance(settings, dict)
        required_keys = ["server_name", "version", "capabilities", "max_connections", "timeout"]
        for key in required_keys:
            assert key in settings
        
        # Verify settings values
        assert settings["server_name"] == "Example MCP Server"
        assert settings["version"] == "0.1.0"
        assert isinstance(settings["capabilities"], list)
        assert "calculate" in settings["capabilities"]
        assert "greet" in settings["capabilities"]
    
    def test_server_info_resource(self):
        """Test the server info resource."""        
        info = get_server_info()
        
        # Verify info structure
        assert isinstance(info, dict)
        required_keys = ["name", "description", "author", "license"]
        for key in required_keys:
            assert key in info
        
        # Verify info values
        assert info["name"] == "Example MCP Server"
        assert info["license"] == "MIT"
        assert "FastMCP" in info["description"]


class TestServerPrompts:
    """Test server prompt endpoints."""
    
    def test_help_prompt(self):
        """Test the help prompt."""        
        help_text = help_prompt()
        
        # Verify help structure
        assert isinstance(help_text, str)
        assert len(help_text) > 0
        
        # Verify help content
        assert "MCP Server Help" in help_text
        assert "Tools:" in help_text
        assert "Resources:" in help_text
        assert "Prompts:" in help_text
        assert "calculate" in help_text
        assert "greet" in help_text


@pytest.mark.asyncio
class TestAsyncIntegration:
    """Test asynchronous integration scenarios."""
    
    async def test_concurrent_calculations(self):
        """Test concurrent calculation requests."""
        import asyncio
        
        async def async_calculate(expression: str) -> str:
            # Simulate async calculation (in real FastMCP, this might be async)
            await asyncio.sleep(0.01)  # Small delay to simulate async work
            return calculate(expression)
        
        # Run multiple calculations concurrently
        expressions = ["1+1", "2*3", "4+5", "6/2", "7-3"]
        tasks = [async_calculate(expr) for expr in expressions]
        results = await asyncio.gather(*tasks)
        
        # Verify all results
        assert len(results) == 5
        for result in results:
            assert "The result of" in result or "Error" in result
    
    async def test_concurrent_greetings(self):
        """Test concurrent greeting requests."""
        import asyncio
        
        async def async_greet(name: str) -> str:
            # Simulate async greeting
            await asyncio.sleep(0.01)
            return greet(name)
        
        # Run multiple greetings concurrently
        names = ["Alice", "Bob", "Charlie", "Diana", "Eve"]
        tasks = [async_greet(name) for name in names]
        results = await asyncio.gather(*tasks)
        
        # Verify all results
        assert len(results) == 5
        for i, result in enumerate(results):
            assert f"Hello, {names[i]}!" in result