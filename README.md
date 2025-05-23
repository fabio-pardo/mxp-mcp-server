# MCP Server Template

A template for creating a Model Context Protocol (MCP) server that can be deployed in a container.

## Usage

### Endpoints
- `GET /` — Health check, returns server status
- `GET /healthz` — Health check, returns OK
- `POST /mcp` — Main MCP endpoint (accepts JSON with action and parameters)

### Example: List Resources
```
POST /mcp
{
  "action": "list_resources",
  "parameters": {}
}
```

### Example: Read Resource (Account)
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

### Running the Server (Docker)
1. Build the container:
   ```sh
   docker build -t mxp-mcp-server .
   ```
2. Run the container:
   ```sh
   docker run -p 8000:8000 mxp-mcp-server
   ```
3. The server will be available at `http://localhost:8000/`

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
