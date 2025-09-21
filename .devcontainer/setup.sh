#!/bin/bash

echo "🚀 Finalizing Development Environment Setup"
echo "==========================================="

# Set up pre-commit hooks
echo "🔗 Setting up pre-commit hooks..."
pre-commit install 2>/dev/null || echo "ℹ️  Pre-commit hooks setup skipped (no .pre-commit-config.yaml)"

# Get the current workspace directory
WORKSPACE_DIR=$(pwd)

# Create useful aliases
echo "⚡ Setting up development aliases..."
cat >> ~/.zshrc << EOF

# Formation Dev Augmenté Aliases
alias start-loan="cd ${WORKSPACE_DIR} && python start-loan-simulator.py"
alias start-api="cd ${WORKSPACE_DIR} && python start-interest-rate-api.py"
alias start-both="cd ${WORKSPACE_DIR} && python start-both.py"
alias loan-logs="cd ${WORKSPACE_DIR}/loan-simulator && python main.py"
alias api-logs="cd ${WORKSPACE_DIR}/interest-rate-api && python main.py"
alias test-loan="cd ${WORKSPACE_DIR}/loan-simulator && pytest"
alias test-api="cd ${WORKSPACE_DIR}/interest-rate-api && pytest"
alias format-code="black . && isort . && flake8 ."

EOF

# Create workspace settings for VS Code
echo "⚙️  Configuring VS Code workspace settings..."
mkdir -p .vscode
cat > .vscode/settings.json << 'EOF'
{
    "python.terminal.activateEnvironment": true,
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": [
        "."
    ],
    "python.testing.unittestEnabled": false,
    "python.testing.autoTestDiscoverOnSaveEnabled": true,
    "files.watcherExclude": {
        "**/.git/objects/**": true,
        "**/.git/subtree-cache/**": true,
        "**/node_modules/*/**": true,
        "**/__pycache__/**": true,
        "**/.pytest_cache/**": true
    }
}
EOF

# Create launch configuration for debugging
cat > .vscode/launch.json << 'EOF'
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Debug Loan Simulator",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/loan-simulator/main.py",
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}",
            "env": {
                "PYTHONPATH": "${workspaceFolder}"
            }
        },
        {
            "name": "Debug Interest Rate API",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/interest-rate-api/main.py",
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}",
            "env": {
                "PYTHONPATH": "${workspaceFolder}"
            }
        },
        {
            "name": "Debug Start Both",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/start-both.py",
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}",
            "env": {
                "PYTHONPATH": "${workspaceFolder}"
            }
        }
    ]
}
EOF

# Create development tasks
cat > .vscode/tasks.json << 'EOF'
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Start Loan Simulator",
            "type": "shell",
            "command": "python",
            "args": ["start-loan-simulator.py"],
            "group": "build",
            "presentation": {
                "echo": true,
                "reveal": "always",
                "focus": false,
                "panel": "new",
                "showReuseMessage": true,
                "clear": false
            },
            "problemMatcher": []
        },
        {
            "label": "Start Interest Rate API",
            "type": "shell",
            "command": "python",
            "args": ["start-interest-rate-api.py"],
            "group": "build",
            "presentation": {
                "echo": true,
                "reveal": "always",
                "focus": false,
                "panel": "new",
                "showReuseMessage": true,
                "clear": false
            },
            "problemMatcher": []
        },
        {
            "label": "Start Both Applications",
            "type": "shell",
            "command": "python",
            "args": ["start-both.py"],
            "group": {
                "kind": "build",
                "isDefault": true
            },
            "presentation": {
                "echo": true,
                "reveal": "always",
                "focus": false,
                "panel": "new",
                "showReuseMessage": true,
                "clear": false
            },
            "problemMatcher": []
        },
        {
            "label": "Format Code",
            "type": "shell",
            "command": "black",
            "args": ["."],
            "group": "build",
            "presentation": {
                "echo": true,
                "reveal": "silent",
                "focus": false,
                "panel": "shared",
                "showReuseMessage": true,
                "clear": false
            },
            "problemMatcher": []
        },
        {
            "label": "Lint Code",
            "type": "shell",
            "command": "flake8",
            "args": ["."],
            "group": "test",
            "presentation": {
                "echo": true,
                "reveal": "always",
                "focus": false,
                "panel": "shared",
                "showReuseMessage": true,
                "clear": false
            },
            "problemMatcher": []
        }
    ]
}
EOF

echo ""
echo "✅ Development environment setup completed!"
echo ""
echo "🎯 Quick Start Commands:"
echo "  start-both     → Start both applications"
echo "  start-loan     → Start loan simulator only"
echo "  start-api      → Start interest rate API only"
echo "  format-code    → Format and lint code"
echo ""
echo "🌐 Application URLs:"
echo "  Loan Simulator: http://localhost:8080"
echo "  Interest Rate API: http://localhost:8081"
echo "  API Documentation: http://localhost:8081/swagger-ui.html"
echo ""
echo "🚀 Ready to code!"