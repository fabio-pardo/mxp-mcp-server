# Virgin Voyages MXP-MCP Server

A Model Context Protocol (MCP) server that provides a REST API interface to the Virgin Voyages MXP system. This server exposes MXP functionality through convenient API endpoints while maintaining the MCP standard.

## Usage

### Endpoints

#### MCP Endpoints
- `GET /` — Health check, returns server status
- `GET /healthz` — Health check, returns OK
- `POST /mcp` — Main MCP endpoint (accepts JSON with action and parameters)

#### MXP API Endpoints
- `GET /account/{charge_id}` — Get account information by charge ID
- `GET /crew` — Get crew information
- `GET /folio/{folio_id}` — Get folio information by folio ID
- `GET /document/{document_id}` — Get document information by document ID
- `GET /icafe` — Get iCafe information (optional: ?icafe_id=123)
- `GET /person_image/{person_id}` — Get person image by person ID
- `GET /quick_code` — Get quick code information
- `GET /sailor_manifest` — Get sailor manifest information
- `GET /receipt_image/{receipt_id}` — Get receipt image by receipt ID
- `GET /person_invoice/{person_id}` — Get person invoice by person ID

### Example: List Resources via MCP
```
POST /mcp
{
  "action": "list_resources",
  "parameters": {}
}
```

### Example: Read Resource (Account) via MCP
```
POST /mcp
{
  "action": "read_resource",
  "parameters": {
    "resource_type": "account",
    "charge_id": 10000004
  }
}
```

### Environment Variables Configuration

The server uses environment variables for configuration which can be set in a `.env` file in the project root:

```sh
# .env file example
MXP_BASE_URL=http://api.example.com/mxp/api
MXP_USERNAME=example_user
MXP_PASSWORD=example_password
```

Key environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `MXP_BASE_URL` | Base URL for the MXP API | http://localhost/api |
| `MXP_USERNAME` | Username for MXP API authentication | username |
| `MXP_PASSWORD` | Password for MXP API authentication | password |
| `PORT` | Port for the server to listen on | 8000 |

### Running the Server

#### Local Development
```sh
# Ensure dependencies are installed
pip install -r requirements.txt

# Run the server
python server.py
```

#### Using Docker
```sh
# Build and run with Docker
docker build -t mxp-mcp-server .
docker run -p 8000:8000 --env-file .env mxp-mcp-server
```

#### Using Docker Compose (Recommended)
```sh
# Build and start the server with Docker Compose
docker-compose up --build
```

The server will be available at `http://localhost:8000/`

### OpenAPI Docs
FastAPI automatically provides OpenAPI docs at:
- `http://localhost:8000/docs` (Swagger UI)
- `http://localhost:8000/redoc` (ReDoc)

## What is an MCP Server?

The Model Context Protocol (MCP) is a standard that connects AI systems with external tools and data sources. MCP servers extend AI capabilities by providing access to specialized functions, external information, and services.

## Project Structure

```
mcp-server/
├── Dockerfile           # Container definition
├── requirements.txt     # Python dependencies
├── server.py            # Main server implementation
├── tools/               # Directory for tool implementations
│   ├── __init__.py
│   └── example_tool.py  # Example tool implementation
└── README.md            # This file
```

## Getting Started

### Local Development

1. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the server:
   ```
   python server.py
   ```

   The server will start on http://localhost:8000

### Docker Deployment

1. Build the Docker image:
   ```
   docker build -t mcp-server .
   ```

2. Run the container:
   ```
   docker run -p 8000:8000 mcp-server
   ```

   The server will be accessible at http://localhost:8000

## API Endpoints

- `GET /`: Server status
- `GET /healthz`: Health check endpoint
- `POST /mcp`: Main MCP request endpoint
- `GET /list-tools`: List available tools
- `POST /debug`: Debug endpoint that echoes back the request

## Adding New Tools

To add a new tool:

1. Create a new file in the `tools/` directory (e.g., `tools/my_tool.py`)
2. Implement your tool class with an `execute()` method
3. Import and initialize your tool in `server.py`
4. Add a new condition in the `/mcp` endpoint handler to dispatch requests to your tool
5. Update the tool list in the `/list-tools` endpoint

## Example Request

```bash
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "action": "example_tool",
    "parameters": {
      "message": "Hello, MCP!"
    }
  }'
```

Expected response:
```json
{
  "result": {
    "echo": "Hello, MCP!",
    "timestamp": "2025-05-21T13:49:25-04:00"
  },
  "error": null,
  "metadata": null
}
```

## Deployment Considerations

- Set environment variables for configuration in production
- Consider using a production-grade ASGI server for deployment
- Implement proper authentication for production deployments
