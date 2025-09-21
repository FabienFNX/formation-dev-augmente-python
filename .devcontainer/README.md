# Development Container Configuration

This directory contains the configuration for a GitHub Codespaces / VS Code Dev Container environment optimized for Python FastAPI development.

## What's Included

### Base Environment
- **Python 3.11** on Debian Bullseye
- **Zsh** with Oh My Zsh for enhanced terminal experience
- **Git** and **GitHub CLI** for version control and GitHub integration

### Python Development Tools
- **FastAPI** and **Uvicorn** for web development
- **Black** for code formatting
- **Flake8** for linting
- **isort** for import sorting
- **Pylint** for additional code analysis
- **pytest** for testing
- **pre-commit** for git hooks

### VS Code Extensions
- Python language support with IntelliSense
- Formatting and linting tools
- REST client for API testing
- Live server for frontend development
- GitHub Copilot integration
- Jupyter notebooks support

### Pre-configured Features
- **Port forwarding** for both applications (8080, 8081)
- **Custom aliases** for quick development commands
- **VS Code tasks** for common operations
- **Debug configurations** for both applications
- **Automatic dependency installation**

## Quick Start

1. **Open in Codespaces**: Click "Code" → "Codespaces" → "Create codespace on main"
2. **Wait for setup**: The environment will automatically install all dependencies
3. **Start developing**: Use the provided aliases and tasks

## Development Commands

Once the container is ready, you can use these commands:

```bash
# Start both applications
start-both

# Start individual applications
start-loan     # Loan simulator (port 8080)
start-api      # Interest rate API (port 8081)

# Development tools
format-code    # Format and lint all code
test-loan      # Run loan simulator tests
test-api       # Run interest rate API tests
```

## VS Code Integration

### Tasks (Ctrl+Shift+P → "Tasks: Run Task")
- **Start Both Applications** (default build task)
- **Start Loan Simulator**
- **Start Interest Rate API**
- **Format Code**
- **Lint Code**

### Debug Configurations (F5)
- **Debug Loan Simulator**
- **Debug Interest Rate API**

## Port Configuration

The container automatically forwards these ports:

- **8080**: Loan Simulator (Frontend + API)
- **8081**: Interest Rate API

## File Structure

```
.devcontainer/
├── devcontainer.json    # Main container configuration
├── setup.sh            # Post-creation setup script
└── README.md           # This file
```

## Customization

You can modify the container configuration by editing:

- `devcontainer.json` - Main container settings, extensions, and features
- `setup.sh` - Post-creation setup commands and tool installation

## Troubleshooting

### Container Won't Start
- **OCI runtime exec failed**: This usually means the workspace folder path is incorrect
  - The container automatically detects the correct workspace directory
  - No manual path configuration needed
- Check that the base image is available
- Verify JSON syntax in `devcontainer.json`

### Dependencies Not Installing
- Check `setup.sh` for any failed commands
- Manually run setup commands in the terminal
- Ensure both `requirements.txt` files exist in their respective directories

### Port Not Accessible
- Ensure the application is running on `0.0.0.0` (not `127.0.0.1`)
- Check that ports are properly forwarded in the configuration
- Verify the applications are actually starting (check terminal output)

### VS Code Extensions Not Loading
- Restart the container if extensions don't install
- Check the "Extensions" tab for any failed installations
- Some extensions may require a window reload (Ctrl+Shift+P → "Developer: Reload Window")

## Environment Variables

The container sets up the following environment:

- `PYTHONPATH`: Includes the workspace root
- Shell aliases for quick development commands
- VS Code settings for Python development

This development container provides a complete, ready-to-use environment for FastAPI development with all necessary tools and configurations pre-installed.