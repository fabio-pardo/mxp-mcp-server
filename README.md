# Virgin Voyages MXP-MCP Server

A **proper Model Context Protocol (MCP) server** and REST API for the Virgin Voyages MXP system. This project provides both MCP-compliant tools for LLM integration (Claude Desktop, etc.) and traditional REST API endpoints for backward compatibility.

## 🎯 What is This?

This server exposes Virgin Voyages MXP system functionality in two ways:

1. **MCP Server** - For AI assistants (Claude Desktop, Cursor, etc.) to directly access MXP data as tools
2. **REST API** - Traditional HTTP endpoints for web applications and existing integrations

## 📁 Project Structure

```
mxp-mcp-server/
├── src/
│   ├── mcp_server/          # MCP server implementation
│   │   ├── __init__.py
│   │   └── server.py        # Main MCP server with tools, resources, prompts
│   ├── rest_api/            # Traditional REST API
│   │   ├── __init__.py
│   │   └── server.py        # FastAPI REST endpoints
│   └── shared/              # Shared MXP client logic
│       ├── __init__.py
│       └── mxp_client.py    # MXP HTTP client with authentication
├── .env                     # Environment variables (create from .env.example)
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── README.md
└── uv.lock
```

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- UV package manager (recommended) or pip
- Access to Virgin Voyages MXP system

### Installation

```bash
# Clone the repository
git clone https://github.com/fabio-pardo/mxp-mcp-server.git
cd mxp-mcp-server

# Install dependencies
uv sync  # or: pip install -r requirements.txt

# Create .env file with your credentials
cp .env.example .env
# Edit .env with your MXP credentials
```

### Environment Variables

Create a `.env` file in the project root:

```env
# MXP System Configuration
MXP_BASE_URL=http://your-mxp-server/API/MXP_Virgin.exe
MXP_USERNAME=your_username
MXP_PASSWORD=your_password

# Server Configuration
PORT=8000
```

## 🎮 Usage

### Option 1: MCP Server (for Claude Desktop, AI Tools)

The MCP server exposes MXP functionality as **tools** that AI assistants can call directly.

#### Run with stdio (for Claude Desktop):

```bash
# Run MCP server
python src/mcp_server/server.py --transport stdio

# Or with UV
uv run python src/mcp_server/server.py --transport stdio
```

#### Run with streamable-http (for web clients):

```bash
# Run with uvicorn
uvicorn src.mcp_server.server:mcp.streamable_http_app --host 0.0.0.0 --port 8000
```

#### Configure Claude Desktop

Add to your Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "virgin-voyages-mxp": {
      "command": "python",
      "args": [
        "/path/to/mxp-mcp-server/src/mcp_server/server.py",
        "--transport",
        "stdio"
      ],
      "env": {
        "MXP_BASE_URL": "http://your-mxp-server/API/MXP_Virgin.exe",
        "MXP_USERNAME": "your_username",
        "MXP_PASSWORD": "your_password"
      }
    }
  }
}
```

### Option 2: REST API Server (for HTTP clients)

The REST API provides traditional HTTP endpoints for web applications.

```bash
# Run REST API server
python src/rest_api/server.py

# Or with uvicorn
uvicorn src.rest_api.server:app --host 0.0.0.0 --port 8000 --reload
```

### Option 3: Docker

```bash
# Build and run with Docker Compose
docker-compose up --build

# Or with Docker
docker build -t mxp-mcp-server .
docker run -p 8000:8000 --env-file .env mxp-mcp-server
```

## 📖 API Documentation

### MCP Server Tools

When connected via MCP, the following tools are available to AI assistants:

| Tool | Description | Parameters |
|------|-------------|------------|
| `get_account_info` | Get account information | `charge_id: int` |
| `get_crew_info` | Get crew member information | None |
| `get_folio_info` | Get folio details | `folio_id: int` |
| `get_document_info` | Get document information | `document_id: int` |
| `get_icafe_info` | Get iCafe session data | `icafe_id: int \| None` |
| `get_person_image` | Get person image | `person_id: int` |
| `get_quick_code_info` | Get quick codes | None |
| `get_manifest_info` | Get sailor manifest | None |
| `get_receipt_image_info` | Get receipt image | `receipt_id: int` |
| `get_person_invoice_info` | Get person invoice | `person_id: int` |

### MCP Resources

Resources provide contextual information to LLMs:

- `mxp://config/info` - System configuration and available tools
- `mxp://help/tools` - Detailed usage guide for all tools

### MCP Prompts

Pre-built prompt templates for common tasks:

- `analyze_account(charge_id)` - Generate account analysis prompt
- `review_folio(folio_id)` - Generate folio review prompt
- `crew_report()` - Generate crew report prompt

### REST API Endpoints

#### Health Checks

- `GET /` - Server status
- `GET /healthz` - Health check

#### MXP Data Endpoints

- `GET /account/{charge_id}` - Get account information
- `GET /crew` - Get crew information
- `GET /folio/{folio_id}` - Get folio information
- `GET /document/{document_id}` - Get document information
- `GET /icafe?icafe_id=123` - Get iCafe information (optional ID)
- `GET /person-image/{person_id}` - Get person image
- `GET /quick-code` - Get quick code information
- `GET /sailor-manifest` - Get sailor manifest
- `GET /receipt-image/{receipt_id}` - Get receipt image
- `GET /person-invoice/{person_id}` - Get person invoice

#### OpenAPI Documentation

When running the REST API server, visit:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🔧 Development

### Project Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
uv sync

# Install pre-commit hooks (optional)
pre-commit install
```

### Running Tests

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=src
```

### Type Checking

```bash
# Run type checker
basedpyright src/
```

## 🌟 MCP vs REST API - When to Use Each

### Use MCP Server When:

✅ Integrating with AI assistants (Claude Desktop, Cursor, Windsurf)  
✅ Building LLM-powered workflows  
✅ Enabling natural language access to MXP data  
✅ Creating AI agents that need MXP access  
✅ You want automatic tool discovery and validation

### Use REST API When:

✅ Building web applications  
✅ Mobile app integrations  
✅ Traditional HTTP clients  
✅ Existing integrations that expect REST endpoints  
✅ You need direct HTTP access

## 🔒 Security

- **Never commit credentials** - Use `.env` file (gitignored)
- **Change default passwords** - Always use strong, unique passwords
- **Use HTTPS in production** - Configure reverse proxy (nginx, traefik)
- **Implement rate limiting** - Protect against abuse
- **Monitor access logs** - Track API usage

## 📝 Example Usage

### Using MCP with Claude Desktop

Once configured, simply ask Claude:

```
"What's the account balance for charge ID 10000004?"
"Show me the crew information"
"Analyze folio 5678"
```

Claude will automatically use the appropriate tools!

### Using REST API with cURL

```bash
# Get account information
curl http://localhost:8000/account/10000004

# Get crew info
curl http://localhost:8000/crew

# Get folio with auth (if needed)
curl -u username:password http://localhost:8000/folio/5678
```

### Using REST API with Python

```python
import requests

# Get account information
response = requests.get("http://localhost:8000/account/10000004")
account_data = response.json()
print(account_data)

# Get crew information
response = requests.get("http://localhost:8000/crew")
crew_data = response.json()
print(crew_data)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📜 License

This project is proprietary to Virgin Voyages.

## 🆘 Support

For issues, questions, or contributions:

- Open an issue on GitHub
- Contact: [Your Contact Info]

## 🎓 Learn More

### About Model Context Protocol (MCP)

- [Official MCP Documentation](https://modelcontextprotocol.io)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [Claude Desktop MCP Guide](https://docs.anthropic.com/claude/docs/model-context-protocol)

### About FastAPI

- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [Pydantic Documentation](https://docs.pydantic.dev)

---

**Built with ❤️ for Virgin Voyages**
