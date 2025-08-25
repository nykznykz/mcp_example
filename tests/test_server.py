"""Test cases for server utilities and configuration."""

import logging
from unittest.mock import patch

import pytest

from mcp_server.server import ServerConfig, setup_logging


class TestServerConfig:
    """Test cases for ServerConfig class."""

    def test_server_config_initialization(self):
        """Test ServerConfig initialization with default values."""
        config = ServerConfig()

        assert config.name == "Example MCP Server"
        assert config.version == "0.1.0"
        assert config.max_connections == 100
        assert config.timeout == 30
        assert config.log_level == logging.INFO

    def test_server_config_to_dict(self):
        """Test ServerConfig to_dict method."""
        config = ServerConfig()
        config_dict = config.to_dict()

        expected_keys = {"name", "version", "max_connections", "timeout", "log_level"}
        assert set(config_dict.keys()) == expected_keys
        assert config_dict["name"] == "Example MCP Server"
        assert config_dict["version"] == "0.1.0"
        assert config_dict["max_connections"] == 100
        assert config_dict["timeout"] == 30
        assert config_dict["log_level"] == logging.INFO

    def test_server_config_modification(self):
        """Test ServerConfig value modification."""
        config = ServerConfig()
        config.name = "Custom Server"
        config.max_connections = 50

        assert config.name == "Custom Server"
        assert config.max_connections == 50

        config_dict = config.to_dict()
        assert config_dict["name"] == "Custom Server"
        assert config_dict["max_connections"] == 50


class TestSetupLogging:
    """Test cases for setup_logging function."""

    @patch("mcp_server.server.logging.basicConfig")
    @patch("mcp_server.server.logging.getLogger")
    def test_setup_logging_default_level(self, mock_get_logger, mock_basic_config):
        """Test setup_logging with default level."""
        mock_logger = mock_get_logger.return_value

        setup_logging()

        # Verify basicConfig was called with correct parameters
        mock_basic_config.assert_called_once_with(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # Verify specific loggers were configured
        assert mock_get_logger.call_count >= 2
        mock_logger.setLevel.assert_called()

    @patch("mcp_server.server.logging.basicConfig")
    @patch("mcp_server.server.logging.getLogger")
    def test_setup_logging_custom_level(self, mock_get_logger, mock_basic_config):
        """Test setup_logging with custom level."""
        mock_logger = mock_get_logger.return_value

        setup_logging(level=logging.DEBUG)

        # Verify basicConfig was called with DEBUG level
        mock_basic_config.assert_called_once_with(
            level=logging.DEBUG,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # Verify loggers were set to DEBUG level
        mock_logger.setLevel.assert_called_with(logging.DEBUG)

    @patch("mcp_server.server.logging.basicConfig")
    @patch("mcp_server.server.logging.getLogger")
    def test_setup_logging_logger_names(self, mock_get_logger, mock_basic_config):
        """Test that setup_logging configures the correct logger names."""
        setup_logging()

        # Check that the correct logger names were requested
        logger_calls = [call[0][0] for call in mock_get_logger.call_args_list]
        assert "mcp_server" in logger_calls
        assert "fastmcp" in logger_calls

    @pytest.mark.parametrize(
        "log_level",
        [
            logging.DEBUG,
            logging.INFO,
            logging.WARNING,
            logging.ERROR,
            logging.CRITICAL,
        ],
    )
    @patch("mcp_server.server.logging.basicConfig")
    def test_setup_logging_various_levels(self, mock_basic_config, log_level):
        """Test setup_logging with various log levels."""
        setup_logging(level=log_level)

        mock_basic_config.assert_called_once()
        args, kwargs = mock_basic_config.call_args
        assert kwargs["level"] == log_level
