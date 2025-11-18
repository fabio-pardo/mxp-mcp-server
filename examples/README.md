# MCP Server Examples

## Example 1: Using MCP with Claude Desktop

### Claude Desktop Configuration

Add this to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "virgin-voyages-mxp": {
      "command": "python",
      "args": [
        "/Users/fabio/dev/virgin_voyages/mxp-mcp-server/src/mcp_server/server.py",
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

### Example Prompts for Claude

Once configured, you can ask Claude:

1. **"What's the account information for charge ID 10000004?"**
   - Claude will use `get_account_info(10000004)`

2. **"Show me the crew information"**
   - Claude will use `get_crew_info()`

3. **"Get folio details for folio ID 5678"**
   - Claude will use `get_folio_info(5678)`

4. **"Analyze the account with charge ID 10000004"**
   - Claude will use the `analyze_account` prompt template

## Example 2: Python MCP Client

```python
import asyncio
from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client


async def main():
    # Connect to MCP server
    server_params = StdioServerParameters(
        command="python",
        args=["src/mcp_server/server.py", "--transport", "stdio"],
        env={
            "MXP_BASE_URL": "http://your-mxp-server/API/MXP_Virgin.exe",
            "MXP_USERNAME": "your_username",
            "MXP_PASSWORD": "your_password",
        }
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize session
            await session.initialize()
            
            # List available tools
            tools = await session.list_tools()
            print("Available tools:")
            for tool in tools.tools:
                print(f"  - {tool.name}: {tool.description}")
            
            # Call a tool
            result = await session.call_tool(
                "get_account_info",
                {"charge_id": 10000004}
            )
            print(f"\nAccount info: {result.content}")
            
            # List resources
            resources = await session.list_resources()
            print("\nAvailable resources:")
            for resource in resources.resources:
                print(f"  - {resource.uri}: {resource.name}")
            
            # Read a resource
            config = await session.read_resource("mxp://config/info")
            print(f"\nConfig: {config.contents}")


if __name__ == "__main__":
    asyncio.run(main())
```

## Example 3: REST API Usage

### cURL Examples

```bash
# Get account information
curl http://localhost:8000/account/10000004

# Get crew information
curl http://localhost:8000/crew

# Get folio with pretty printing
curl http://localhost:8000/folio/5678 | jq '.'

# Get iCafe info with optional ID
curl http://localhost:8000/icafe?icafe_id=123
```

### Python Requests Example

```python
import requests

BASE_URL = "http://localhost:8000"

# Get account information
response = requests.get(f"{BASE_URL}/account/10000004")
if response.status_code == 200:
    account = response.json()
    print(f"Account: {account}")
else:
    print(f"Error: {response.status_code}")

# Get crew information
response = requests.get(f"{BASE_URL}/crew")
crew = response.json()
print(f"Crew: {crew}")

# Get folio information
response = requests.get(f"{BASE_URL}/folio/5678")
folio = response.json()
print(f"Folio: {folio}")
```

### JavaScript/TypeScript Example

```javascript
// Fetch account information
const getAccount = async (chargeId) => {
  const response = await fetch(`http://localhost:8000/account/${chargeId}`);
  const data = await response.json();
  return data;
};

// Get crew information
const getCrew = async () => {
  const response = await fetch('http://localhost:8000/crew');
  const data = await response.json();
  return data;
};

// Usage
getAccount(10000004).then(account => {
  console.log('Account:', account);
});

getCrew().then(crew => {
  console.log('Crew:', crew);
});
```

## Example 4: Using with Streamable HTTP

### Start Server

```bash
uvicorn src.mcp_server.server:mcp.streamable_http_app --host 0.0.0.0 --port 8001
```

### Connect with MCP Client

```python
import asyncio
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client


async def connect_via_http():
    async with streamable_http_client("http://localhost:8001/mcp") as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # List tools
            tools = await session.list_tools()
            print(f"Tools: {[t.name for t in tools.tools]}")
            
            # Call tool
            result = await session.call_tool("get_account_info", {"charge_id": 10000004})
            print(f"Result: {result.content}")


asyncio.run(connect_via_http())
```

## Example 5: Docker Deployment

### Using Docker Compose

```bash
# Start both REST API and MCP Server
docker-compose up -d

# REST API available at: http://localhost:8000
# MCP Server available at: http://localhost:8001/mcp

# View logs
docker-compose logs -f

# Stop servers
docker-compose down
```

### Using Docker Run

```bash
# Build image
docker build -t mxp-mcp-server .

# Run REST API
docker run -d \
  -p 8000:8000 \
  --env-file .env \
  --name mxp-rest-api \
  mxp-mcp-server

# Run MCP Server
docker run -d \
  -p 8001:8000 \
  --env-file .env \
  --name mxp-mcp-server \
  mxp-mcp-server \
  uv run uvicorn src.mcp_server.server:mcp.streamable_http_app --host 0.0.0.0 --port 8000
```

## Example 6: Error Handling

### Python with Error Handling

```python
import requests
from requests.exceptions import RequestException

def get_account_safe(charge_id: int):
    try:
        response = requests.get(
            f"http://localhost:8000/account/{charge_id}",
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except RequestException as e:
        print(f"Error fetching account: {e}")
        return None

# Usage
account = get_account_safe(10000004)
if account:
    print(f"Success: {account}")
else:
    print("Failed to fetch account")
```

## Example 7: Batch Requests

### Get Multiple Accounts

```python
import asyncio
import aiohttp

async def get_multiple_accounts(charge_ids: list[int]):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for charge_id in charge_ids:
            task = session.get(f"http://localhost:8000/account/{charge_id}")
            tasks.append(task)
        
        responses = await asyncio.gather(*tasks)
        results = []
        for response in responses:
            if response.status == 200:
                results.append(await response.json())
        
        return results

# Usage
charge_ids = [10000004, 10000005, 10000006]
accounts = asyncio.run(get_multiple_accounts(charge_ids))
print(f"Fetched {len(accounts)} accounts")
```
