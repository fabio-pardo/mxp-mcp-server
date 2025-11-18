#!/usr/bin/env bash
# Quick start script for Virgin Voyages MXP-MCP Server

set -e

echo "🚀 Virgin Voyages MXP-MCP Server Setup"
echo "======================================"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
  echo "⚠️  No .env file found. Creating from .env.example..."
  cp .env.example .env
  echo "✅ Created .env file. Please update it with your MXP credentials."
  echo ""
  read -p "Press Enter to continue after updating .env..."
fi

# Check for UV
if ! command -v uv &>/dev/null; then
  echo "📦 UV package manager not found. Installing..."
  pip install uv
fi

# Install dependencies
echo "📦 Installing dependencies..."
uv sync

echo ""
echo "✅ Setup complete!"
echo ""
echo "Choose how to run the server:"
echo ""
echo "1. MCP Server (for Claude Desktop, AI tools)"
echo "   python src/mcp_server/server.py --transport stdio"
echo ""
echo "2. REST API Server (for web applications)"
echo "   python src/rest_api/server.py"
echo ""
echo "3. Docker (both servers)"
echo "   docker-compose up --build"
echo ""
read -p "Enter your choice (1-3): " choice

case $choice in
1)
  echo "🤖 Starting MCP Server..."
  PYTHONPATH="${PYTHONPATH:+${PYTHONPATH}:}$(pwd)/src" python src/mcp_server/server.py --transport stdio
  ;;
2)
  echo "🌐 Starting REST API Server..."
  PYTHONPATH="${PYTHONPATH:+${PYTHONPATH}:}$(pwd)/src" python src/rest_api/server.py
  ;;
3)
  echo "🐳 Starting with Docker..."
  docker-compose up --build
  ;;
*)
  echo "Invalid choice. Please run manually."
  ;;
esac
