"""Test cases for the main MCP server functionality."""

import pytest
from unittest.mock import patch, Mock

from mcp_server.main import _calculate as calculate, _greet as greet, _get_settings as get_settings, _get_server_info as get_server_info, _help_prompt as help_prompt


class TestCalculateTool:
    """Test cases for the calculate tool."""
    
    def test_calculate_simple_addition(self):
        """Test simple addition calculation."""
        result = calculate("2 + 2")
        assert "The result of '2 + 2' is 4" == result
    
    def test_calculate_simple_subtraction(self):
        """Test simple subtraction calculation."""
        result = calculate("10 - 5")
        assert "The result of '10 - 5' is 5" == result
    
    def test_calculate_simple_multiplication(self):
        """Test simple multiplication calculation."""
        result = calculate("3 * 4")
        assert "The result of '3 * 4' is 12" == result
    
    def test_calculate_simple_division(self):
        """Test simple division calculation."""
        result = calculate("15 / 3")
        assert "The result of '15 / 3' is 5" in result
    
    def test_calculate_complex_expression(self):
        """Test complex mathematical expression."""
        result = calculate("(2 + 3) * 4")
        assert "The result of '(2 + 3) * 4' is 20" == result
    
    def test_calculate_decimal_numbers(self):
        """Test calculation with decimal numbers."""
        result = calculate("10.5 + 2.3")
        assert "12.8" in result
    
    def test_calculate_invalid_characters(self):
        """Test calculation with invalid characters."""
        result = calculate("2 + abc")
        assert "Error: Invalid characters" in result
    
    def test_calculate_malicious_input(self):
        """Test calculation with potentially malicious input."""
        result = calculate("import os")
        assert "Error: Invalid characters" in result
    
    def test_calculate_empty_expression(self):
        """Test calculation with empty expression."""
        result = calculate("")
        assert "Error calculating" in result
    
    def test_calculate_division_by_zero(self):
        """Test calculation with division by zero."""
        result = calculate("5 / 0")
        assert "Error calculating" in result
    
    @pytest.mark.parametrize("expression,expected", [
        ("1 + 1", 2),
        ("5 * 3", 15),
        ("12 / 4", 3.0),  # Division returns float
        ("10 - 7", 3),
    ])
    def test_calculate_parametrized(self, expression, expected):
        """Parametrized test for various calculations."""
        result = calculate(expression)
        assert f"The result of '{expression}' is {expected}" == result


class TestGreetTool:
    """Test cases for the greet tool."""
    
    def test_greet_simple_name(self):
        """Test greeting with a simple name."""
        result = greet("World")
        assert result == "Hello, World! Welcome to the MCP server."
    
    def test_greet_empty_name(self):
        """Test greeting with an empty name."""
        result = greet("")
        assert result == "Hello, ! Welcome to the MCP server."
    
    def test_greet_special_characters(self):
        """Test greeting with special characters."""
        result = greet("João")
        assert result == "Hello, João! Welcome to the MCP server."
    
    def test_greet_long_name(self):
        """Test greeting with a very long name."""
        long_name = "A" * 100
        result = greet(long_name)
        expected = f"Hello, {long_name}! Welcome to the MCP server."
        assert result == expected


class TestResources:
    """Test cases for server resources."""
    
    def test_get_settings(self):
        """Test getting server settings."""
        settings = get_settings()
        
        assert isinstance(settings, dict)
        assert "server_name" in settings
        assert "version" in settings
        assert "capabilities" in settings
        assert settings["server_name"] == "Example MCP Server"
        assert settings["version"] == "0.1.0"
        assert "calculate" in settings["capabilities"]
        assert "greet" in settings["capabilities"]
    
    def test_get_server_info(self):
        """Test getting server information."""
        info = get_server_info()
        
        assert isinstance(info, dict)
        assert "name" in info
        assert "description" in info
        assert "author" in info
        assert "license" in info
        assert info["name"] == "Example MCP Server"
        assert info["license"] == "MIT"


class TestPrompts:
    """Test cases for server prompts."""
    
    def test_help_prompt(self):
        """Test help prompt."""
        help_text = help_prompt()
        
        assert isinstance(help_text, str)
        assert "MCP Server Help" in help_text
        assert "calculate" in help_text
        assert "greet" in help_text
        assert "Tools:" in help_text
        assert "Resources:" in help_text
        assert "Prompts:" in help_text


class TestMainFunction:
    """Test cases for the main function."""
    
    @patch('mcp_server.main.mcp')
    @patch('mcp_server.main.logger')
    def test_main_function_success(self, mock_logger, mock_mcp):
        """Test successful execution of main function."""
        from mcp_server.main import main
        
        # Mock the MCP server run method
        mock_mcp.run.return_value = None
        
        main()
        
        # Verify logging and server start
        mock_logger.info.assert_called_with("Starting MCP server...")
        mock_mcp.run.assert_called_once()
    
    @patch('mcp_server.main.mcp')
    @patch('mcp_server.main.logger')
    def test_main_function_keyboard_interrupt(self, mock_logger, mock_mcp):
        """Test main function handling keyboard interrupt."""
        from mcp_server.main import main
        
        # Mock keyboard interrupt
        mock_mcp.run.side_effect = KeyboardInterrupt()
        
        main()
        
        # Verify proper handling
        mock_logger.info.assert_any_call("Starting MCP server...")
        mock_logger.info.assert_any_call("Server interrupted by user")
    
    @patch('mcp_server.main.mcp')
    @patch('mcp_server.main.logger')
    def test_main_function_exception(self, mock_logger, mock_mcp):
        """Test main function handling exceptions."""
        from mcp_server.main import main
        
        # Mock exception
        mock_mcp.run.side_effect = Exception("Test error")
        
        with pytest.raises(Exception, match="Test error"):
            main()
        
        # Verify error logging
        mock_logger.error.assert_called_with("Server error: Test error")