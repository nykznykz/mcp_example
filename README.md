# MCP Server with FastMCP v2.0

A Model Control Protocol (MCP) server implementation using FastMCP v2.0, featuring Docker containerization, comprehensive testing, and CI/CD automation.

## Features

- 🚀 Built with FastMCP v2.0
- 🐳 Docker containerization with multi-stage builds
- 📦 Modern Python packaging with `uv`
- 🧪 Comprehensive test suite with pytest
- 🔄 GitHub Actions CI/CD pipeline
- 🛡️ Security scanning and dependency management
- 📊 Code coverage reporting
- 🔧 Automated code formatting and linting

## Quick Start

### Prerequisites

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) for dependency management
- Docker (optional, for containerization)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd nikolas-mcp
```

2. Install dependencies using uv:
```bash
uv sync
```

3. Run the server:
```bash
uv run python -m mcp_server.main
```

### Using Docker

1. Build the Docker image:
```bash
docker build -t mcp-server .
```

2. Run the container:
```bash
docker run -p 8000:8000 mcp-server
```

3. Or use docker-compose:
```bash
docker-compose up
```

## Available Tools

The MCP server provides the following tools:

### `calculate`
Evaluates mathematical expressions safely.

**Parameters:**
- `expression` (string): Mathematical expression to evaluate

**Example:**
```json
{
  "tool": "calculate",
  "arguments": {
    "expression": "2 + 3 * 4"
  }
}
```

### `greet`
Generates friendly greeting messages.

**Parameters:**
- `name` (string): Name of the person to greet

**Example:**
```json
{
  "tool": "greet",
  "arguments": {
    "name": "World"
  }
}
```

## Resources

- `config://settings` - Server configuration settings
- `info://server` - General server information

## Prompts

- `help` - Display help information about available capabilities

## Development

### Setup Development Environment

```bash
# Install development dependencies
uv sync --dev

# Install pre-commit hooks
uv run pre-commit install
```

### Running Tests

```bash
# Run all tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=src --cov-report=html

# Run specific test file
uv run pytest tests/test_main.py -v
```

### Code Quality

```bash
# Format code
uv run ruff format .

# Lint code
uv run ruff check .

# Type checking
uv run mypy src/
```

### Project Structure

```
nikolas-mcp/
├── src/
│   └── mcp_server/
│       ├── __init__.py
│       ├── main.py          # Main server implementation
│       └── server.py        # Server utilities and config
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Pytest configuration
│   ├── test_main.py         # Main functionality tests
│   ├── test_server.py       # Server utilities tests
│   └── test_integration.py  # Integration tests
├── .github/
│   └── workflows/
│       ├── ci.yml           # CI/CD pipeline
│       └── dependabot.yml   # Dependabot auto-merge
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml           # Project configuration
└── README.md
```

## CI/CD Pipeline

The project includes a comprehensive GitHub Actions pipeline:

- **Lint and Format**: Runs ruff for code formatting and linting
- **Test Suite**: Runs tests across multiple Python versions and OS platforms
- **Security Scan**: Performs security vulnerability scanning
- **Docker Build**: Builds and tests Docker images
- **Auto-publish**: Publishes to PyPI and Docker Hub on release

### Required Secrets

For full CI/CD functionality, configure these GitHub secrets:

- `PYPI_API_TOKEN` - PyPI authentication token
- `DOCKERHUB_USERNAME` - Docker Hub username
- `DOCKERHUB_TOKEN` - Docker Hub access token

## Configuration

### Environment Variables

- `LOG_LEVEL` - Logging level (default: INFO)
- `PYTHONPATH` - Python path for module resolution

### Server Configuration

The server can be configured via the `ServerConfig` class in `src/mcp_server/server.py`:

```python
config = ServerConfig()
config.max_connections = 200
config.timeout = 60
```

## Docker Configuration

### Multi-stage Build

The Dockerfile uses multi-stage builds for optimized image size:

1. **Base stage**: Sets up Python and system dependencies
2. **Dependencies stage**: Installs Python packages with uv
3. **Runtime stage**: Copies application code and runs the server

### Health Checks

The container includes health checks to ensure the server is running correctly.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and ensure they pass
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

If you encounter any issues or have questions:

1. Check the [Issues](../../issues) page for existing problems
2. Create a new issue with detailed information
3. Refer to the [FastMCP documentation](https://github.com/pydantic/FastMCP) for FastMCP-specific questions