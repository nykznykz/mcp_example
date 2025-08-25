"""Server utilities and configuration."""

import logging
from typing import Any

logger = logging.getLogger(__name__)


class ServerConfig:
    """Server configuration class."""

    def __init__(self) -> None:
        self.name = "Example MCP Server"
        self.version = "0.1.0"
        self.max_connections = 100
        self.timeout = 30
        self.log_level = logging.INFO

    def to_dict(self) -> dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            "name": self.name,
            "version": self.version,
            "max_connections": self.max_connections,
            "timeout": self.timeout,
            "log_level": self.log_level,
        }


def setup_logging(level: int = logging.INFO) -> None:
    """Set up logging configuration."""
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Set specific loggers
    logging.getLogger("mcp_server").setLevel(level)
    logging.getLogger("fastmcp").setLevel(level)
