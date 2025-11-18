# 🏗️ Architecture Diagram

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    Virgin Voyages MXP-MCP Server                │
└─────────────────────────────────────────────────────────────────┘

                              ┌─────────────┐
                              │   Clients   │
                              └─────────────┘
                                     │
                    ┌────────────────┼────────────────┐
                    │                │                │
              ┌─────▼─────┐    ┌────▼─────┐    ┌────▼─────┐
              │  Claude    │    │   Web    │    │  Mobile  │
              │  Desktop   │    │   Apps   │    │   Apps   │
              └─────┬─────┘    └────┬─────┘    └────┬─────┘
                    │                │                │
                    │ MCP Protocol   │ HTTP/REST     │ HTTP/REST
                    │                │                │
        ┌───────────▼───────────┐    │                │
        │                       │    │                │
        │  MCP Server (stdio)   │    │                │
        │  Port: stdio stream   │    │                │
        │                       │    │                │
        │  src/mcp_server/      │    │                │
        │  - 10 Tools           │    │                │
        │  - 2 Resources        │    │                │
        │  - 3 Prompts          │    │                │
        └───────────┬───────────┘    │                │
                    │                │                │
                    │                │                │
        ┌───────────▼────────────────▼────────────────▼───────┐
        │                                                      │
        │         Shared MXP Client (src/shared/)             │
        │                                                      │
        │  - HTTP Basic Auth                                  │
        │  - Environment config                               │
        │  - 10 MXP functions                                 │
        │  - Type-safe                                        │
        └───────────┬──────────────────────────────────────────┘
                    │
                    │ HTTPS + Basic Auth
                    │
        ┌───────────▼──────────────┐
        │                          │
        │   Virgin Voyages MXP     │
        │   Backend System         │
        │                          │
        │   http://10.2.225.226/   │
        │   API/MXP_Virgin.exe     │
        │                          │
        └──────────────────────────┘
```

## Component Details

### 1. MCP Server (`src/mcp_server/server.py`)

```
┌─────────────────────────────────────────┐
│         MCP Server (Port: stdio)        │
├─────────────────────────────────────────┤
│                                         │
│  Tools (10):                            │
│  ├─ get_account_info(charge_id)        │
│  ├─ get_crew_info()                    │
│  ├─ get_folio_info(folio_id)           │
│  ├─ get_document_info(document_id)     │
│  ├─ get_icafe_info(icafe_id?)          │
│  ├─ get_person_image(person_id)        │
│  ├─ get_quick_code_info()              │
│  ├─ get_manifest_info()                │
│  ├─ get_receipt_image_info(receipt_id) │
│  └─ get_person_invoice_info(person_id) │
│                                         │
│  Resources (2):                         │
│  ├─ mxp://config/info                  │
│  └─ mxp://help/tools                   │
│                                         │
│  Prompts (3):                           │
│  ├─ analyze_account(charge_id)         │
│  ├─ review_folio(folio_id)             │
│  └─ crew_report()                      │
│                                         │
│  Transports:                            │
│  ├─ stdio (default)                    │
│  ├─ streamable-http                    │
│  └─ sse                                │
└─────────────────────────────────────────┘
```

### 2. REST API Server (`src/rest_api/server.py`)

```
┌─────────────────────────────────────────┐
│       REST API Server (Port: 8000)      │
├─────────────────────────────────────────┤
│                                         │
│  Health Checks:                         │
│  ├─ GET  /                             │
│  └─ GET  /healthz                      │
│                                         │
│  MXP Endpoints:                         │
│  ├─ GET  /account/{charge_id}          │
│  ├─ GET  /crew                         │
│  ├─ GET  /folio/{folio_id}             │
│  ├─ GET  /document/{document_id}       │
│  ├─ GET  /icafe?icafe_id=123           │
│  ├─ GET  /person-image/{person_id}     │
│  ├─ GET  /quick-code                   │
│  ├─ GET  /sailor-manifest              │
│  ├─ GET  /receipt-image/{receipt_id}   │
│  └─ GET  /person-invoice/{person_id}   │
│                                         │
│  Documentation:                         │
│  ├─ GET  /docs (Swagger UI)            │
│  └─ GET  /redoc (ReDoc)                │
│                                         │
│  Features:                              │
│  ├─ OpenAPI documentation              │
│  ├─ CORS middleware                    │
│  ├─ Error handling                     │
│  └─ Type validation                    │
└─────────────────────────────────────────┘
```

### 3. Shared MXP Client (`src/shared/mxp_client.py`)

```
┌─────────────────────────────────────────┐
│           Shared MXP Client             │
├─────────────────────────────────────────┤
│                                         │
│  Functions (10):                        │
│  ├─ get_account(charge_id)             │
│  ├─ get_crew()                         │
│  ├─ get_folio(folio_id)                │
│  ├─ get_document(document_id)          │
│  ├─ get_icafe(icafe_id?)               │
│  ├─ get_person_image_by_id(person_id)  │
│  ├─ get_quick_code()                   │
│  ├─ get_sailor_manifest()              │
│  ├─ get_receipt_image(receipt_id)      │
│  └─ get_person_invoice(person_id)      │
│                                         │
│  Features:                              │
│  ├─ HTTP Basic Authentication          │
│  ├─ Environment variables              │
│  ├─ Type annotations                   │
│  ├─ Error handling                     │
│  └─ Comprehensive docstrings           │
└─────────────────────────────────────────┘
```

## Data Flow

### MCP Request Flow

```
1. Claude Desktop
   │
   ├─ User asks: "Get account 10000004"
   │
   ▼
2. MCP Client (in Claude)
   │
   ├─ Discovers available tools
   ├─ Selects: get_account_info
   ├─ Calls with: {charge_id: 10000004}
   │
   ▼
3. MCP Server (src/mcp_server/server.py)
   │
   ├─ Receives tool call
   ├─ Validates parameters
   ├─ Calls shared client
   │
   ▼
4. Shared Client (src/shared/mxp_client.py)
   │
   ├─ Builds HTTP request
   ├─ Adds authentication
   ├─ Sends to MXP backend
   │
   ▼
5. MXP Backend
   │
   ├─ Processes request
   ├─ Returns account data
   │
   ▼
6. Response flows back through layers
   │
   └─ Claude formats and presents to user
```

### REST Request Flow

```
1. Web/Mobile App
   │
   ├─ HTTP GET /account/10000004
   │
   ▼
2. REST API Server (src/rest_api/server.py)
   │
   ├─ Receives HTTP request
   ├─ Validates parameters
   ├─ Calls shared client
   │
   ▼
3. Shared Client (src/shared/mxp_client.py)
   │
   ├─ Builds HTTP request
   ├─ Adds authentication
   ├─ Sends to MXP backend
   │
   ▼
4. MXP Backend
   │
   ├─ Processes request
   ├─ Returns account data
   │
   ▼
5. Response flows back
   │
   └─ App receives JSON data
```

## Deployment Architecture

### Docker Deployment

```
┌─────────────────────────────────────────────────┐
│              Docker Host                        │
│                                                 │
│  ┌───────────────────────────────────────────┐ │
│  │  Container: mxp-rest-api                  │ │
│  │  Port: 8000 → 8000                        │ │
│  │  Image: mxp-mcp-server                    │ │
│  │  Command: python src/rest_api/server.py   │ │
│  └───────────────────────────────────────────┘ │
│                                                 │
│  ┌───────────────────────────────────────────┐ │
│  │  Container: mxp-mcp-server                │ │
│  │  Port: 8001 → 8000                        │ │
│  │  Image: mxp-mcp-server                    │ │
│  │  Command: uvicorn ... streamable_http_app │ │
│  └───────────────────────────────────────────┘ │
│                                                 │
│  Shared:                                        │
│  - .env file                                    │
│  - Network                                      │
│  - Volumes                                      │
└─────────────────────────────────────────────────┘
```

## File Dependencies

```
server.py (old) ──┐
mxp_api.py (old) ─┼──> REFACTORED INTO:
                  │
                  ├─> src/mcp_server/server.py
                  │   └─> Proper MCP implementation
                  │
                  ├─> src/rest_api/server.py
                  │   └─> Traditional REST API
                  │
                  └─> src/shared/mxp_client.py
                      └─> Shared MXP client
```

---

**Architecture Status: ✅ Production Ready**
