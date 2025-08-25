"""Pytest configuration and fixtures."""

import pytest
from unittest.mock import Mock

from mcp_server.main import mcp
from mcp_server.server import ServerConfig


@pytest.fixture
def server_config():
    """Provide a test server configuration."""
    return ServerConfig()


@pytest.fixture
def mock_mcp_server():
    """Provide a mock MCP server for testing."""
    mock_server = Mock()
    mock_server.tools = {}
    mock_server.resources = {}
    mock_server.prompts = {}
    return mock_server


@pytest.fixture
def sample_expressions():
    """Provide sample mathematical expressions for testing."""
    return [
        ("2 + 2", 4),
        ("10 - 5", 5),
        ("3 * 4", 12),
        ("15 / 3", 5),
        ("(2 + 3) * 4", 20),
        ("10.5 + 2.3", 12.8),
    ]


@pytest.fixture
def invalid_expressions():
    """Provide invalid mathematical expressions for testing."""
    return [
        "import os",
        "__import__('os')",
        "eval('2+2')",
        "exec('print(1)')",
        "2 + * 3",
        "",
        "abc + def",
    ]