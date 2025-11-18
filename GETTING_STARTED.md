# 🚀 Virgin Voyages MXP-MCP Server - Complete Guide

## 📋 Table of Contents

1. [What Changed?](#what-changed)
2. [Quick Start](#quick-start)
3. [MCP Server Usage](#mcp-server-usage)
4. [REST API Usage](#rest-api-usage)
5. [Docker Deployment](#docker-deployment)
6. [Configuration](#configuration)
7. [Troubleshooting](#troubleshooting)

---

## What Changed?

### ⚠️ BREAKING CHANGES

1. **Removed custom `/mcp` POST endpoint** - It was not MCP-compliant
2. **New folder structure** - Code organized into `src/` directory
3. **Separate servers** - MCP and REST now run independently

### ✅ What's New

1. **Real MCP Server** - Works with Claude Desktop and MCP clients
2. **10 MCP Tools** - LLMs can call MXP functions directly
3. **2 MCP Resources** - Contextual information for LLMs
4. **3 MCP Prompts** - Pre-built templates for common tasks
5. **Multiple Transports** - stdio, streamable-http, SSE
6. **Better Documentation** - Examples, guides, and more

### ✅ What Stayed the Same

- REST API endpoints unchanged
- Environment variable configuration
- MXP client authentication
- Docker support

---

## Quick Start

### Option 1: Use the Start Script

```bash
./start.sh
```

This interactive script will:
1. Check for `.env` file
2. Install dependencies
3. Let you choose which server to run

### Option 2: Manual Start

#### MCP Server (for AI assistants)

```bash
# Install dependencies
uv sync

# Start MCP server
python src/mcp_server/server.py --transport stdio
```

#### REST API (for web apps)

```bash
# Install dependencies
uv sync

# Start REST API
python src/rest_api/server.py
```

---

## MCP Server Usage

### What is MCP?

Model Context Protocol (MCP) is a standard that allows AI assistants like Claude to directly access your tools and data. Think of it as a "USB-C port for AI".

### Supported Transports

| Transport | Use Case | Command |
|-----------|----------|---------|
| **stdio** | Claude Desktop, local clients | `--transport stdio` |
| **streamable-http** | Web clients, remote access | `--transport streamable-http` |
| **sse** | Browser-based clients | `--transport sse` |

### Configure for Claude Desktop

1. **Find your config file:**
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`

2. **Add this configuration:**

```json
{
  "mcpServers": {
    "virgin-voyages-mxp": {
      "command": "python",
      "args": [
        "/FULL/PATH/TO/mxp-mcp-server/src/mcp_server/server.py",
        "--transport",
        "stdio"
      ],
      "env": {
        "MXP_BASE_URL": "http://your-server/API/MXP_Virgin.exe",
        "MXP_USERNAME": "your_username",
        "MXP_PASSWORD": "your_password"
      }
    }
  }
}
```

3. **Restart Claude Desktop**

4. **Test it:** Ask Claude: "What tools do you have access to?"

### Available MCP Tools

Once connected, Claude can use these tools:

```
1. get_account_info(charge_id: int)
   - Get account information by charge ID
   
2. get_crew_info()
   - Get crew member information
   
3. get_folio_info(folio_id: int)
   - Get folio details
   
4. get_document_info(document_id: int)
   - Get document information
   
5. get_icafe_info(icafe_id: int | None)
   - Get iCafe session data
   
6. get_person_image(person_id: int)
   - Get person images
   
7. get_quick_code_info()
   - Get quick codes
   
8. get_manifest_info()
   - Get sailor manifest
   
9. get_receipt_image_info(receipt_id: int)
   - Get receipt images
   
10. get_person_invoice_info(person_id: int)
    - Get person invoices
```

### Example Conversations with Claude

```
You: "What's the account balance for charge ID 10000004?"
Claude: *calls get_account_info(10000004)* 
        "The account has a balance of..."

You: "Show me crew information"
Claude: *calls get_crew_info()*
        "Here are the crew members..."

You: "Analyze folio 5678"
Claude: *uses analyze_folio prompt and calls get_folio_info(5678)*
        "Based on the folio data, I can see..."
```

---

## REST API Usage

The traditional REST API remains unchanged and works exactly as before.

### Start REST API Server

```bash
python src/rest_api/server.py
```

Server starts at: `http://localhost:8000`

### Available Endpoints

```
Health Checks:
  GET  /              - Server status
  GET  /healthz       - Health check

MXP Data:
  GET  /account/{charge_id}
  GET  /crew
  GET  /folio/{folio_id}
  GET  /document/{document_id}
  GET  /icafe?icafe_id=123
  GET  /person-image/{person_id}
  GET  /quick-code
  GET  /sailor-manifest
  GET  /receipt-image/{receipt_id}
  GET  /person-invoice/{person_id}

API Docs:
  GET  /docs          - Swagger UI
  GET  /redoc         - ReDoc
```

### Example Requests

#### cURL

```bash
# Get account
curl http://localhost:8000/account/10000004

# Get crew
curl http://localhost:8000/crew

# Get folio with pretty printing
curl http://localhost:8000/folio/5678 | jq '.'
```

#### Python

```python
import requests

# Get account
response = requests.get("http://localhost:8000/account/10000004")
account = response.json()

# Get crew
crew = requests.get("http://localhost:8000/crew").json()
```

#### JavaScript

```javascript
// Get account
fetch('http://localhost:8000/account/10000004')
  .then(res => res.json())
  .then(data => console.log(data));
```

---

## Docker Deployment

### Using Docker Compose (Recommended)

```bash
# Start both servers
docker-compose up -d

# View logs
docker-compose logs -f

# Stop servers
docker-compose down
```

**Servers:**
- REST API: `http://localhost:8000`
- MCP Server: `http://localhost:8001/mcp`

### Using Docker Run

```bash
# Build image
docker build -t mxp-mcp-server .

# Run REST API
docker run -d -p 8000:8000 --env-file .env mxp-mcp-server

# Run MCP Server (streamable-http)
docker run -d -p 8001:8000 --env-file .env mxp-mcp-server \
  uv run uvicorn src.mcp_server.server:mcp.streamable_http_app --host 0.0.0.0
```

---

## Configuration

### Environment Variables

Create a `.env` file:

```env
# MXP System
MXP_BASE_URL=http://your-mxp-server/API/MXP_Virgin.exe
MXP_USERNAME=your_username
MXP_PASSWORD=your_password

# Server
PORT=8000
```

### Security Best Practices

1. **Never commit `.env` file** (already gitignored)
2. **Use strong passwords**
3. **Enable HTTPS in production**
4. **Implement rate limiting**
5. **Monitor access logs**

---

## Troubleshooting

### MCP Server Issues

#### "Claude can't find my server"

1. Check config file path is absolute
2. Restart Claude Desktop completely
3. Check server starts: `python src/mcp_server/server.py --transport stdio`
4. Verify .env variables are set

#### "Tool not found"

1. Make sure MCP server is running
2. Check Claude can list tools: "What tools do you have?"
3. Verify server logs for errors

### REST API Issues

#### "Connection refused"

```bash
# Check if server is running
curl http://localhost:8000/healthz

# Check port isn't in use
lsof -i :8000

# Start server with logs
python src/rest_api/server.py
```

#### "Authentication failed"

1. Check `.env` file has correct credentials
2. Verify MXP server is accessible
3. Test with curl: `curl -v http://localhost:8000/crew`

### Docker Issues

#### "Container won't start"

```bash
# Check logs
docker-compose logs

# Rebuild
docker-compose build --no-cache
docker-compose up
```

#### "Port already in use"

```bash
# Find process using port
lsof -i :8000

# Kill process
kill -9 <PID>

# Or change port in docker-compose.yml
```

### Import Errors

```bash
# Make sure you're in project root
pwd

# Install dependencies
uv sync

# Test imports
python -c "import sys; sys.path.insert(0, 'src'); from shared.mxp_client import get_account"
```

---

## Additional Resources

- **Examples**: See `examples/README.md` for 7 detailed examples

---

## Getting Help

1. Check this guide first
2. Review `examples/README.md`
3. Check server logs
4. Open an issue on GitHub

---

**Happy coding! 🚀**
