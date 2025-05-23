#!/usr/bin/env python3
"""
MCP Server Template
A basic template for creating a Model Context Protocol (MCP) server.
"""

import logging
import os
from typing import Dict, List, Any, Optional, Union

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Import tools
from tools.example_tool import ExampleTool
from tools.knowledge_tool import KnowledgeBaseTool

# Import MXP API functions
from mxp_api import (
    get_account, get_crew, get_folio, get_document, get_icafe,
    get_person_image_by_id, get_quick_code, get_sailor_manifest,
    get_receipt_image, get_person_invoice
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(title="MCP Server Template")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize tools
example_tool = ExampleTool()
knowledge_tool = KnowledgeBaseTool()

# Define model schemas
class MCPRequest(BaseModel):
    action: str = Field(..., description="The action to perform")
    parameters: Dict[str, Any] = Field(default={}, description="Parameters for the action")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Context for the request")

class MCPResponse(BaseModel):
    result: Union[Dict[str, Any], List[Any], str, int, float, bool, None] = Field(..., description="The result of the action")
    error: Optional[str] = Field(default=None, description="Error message if any")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")

# Define routes
@app.get("/")
async def root():
    return {"message": "MCP Server is running"}

@app.get("/healthz")
async def health_check():
    return {"status": "healthy"}

@app.post("/mcp", response_model=MCPResponse)
async def handle_mcp_request(request: MCPRequest):
    """
    Handle MCP requests.
    """
    try:
        action = request.action
        parameters = request.parameters
        context = request.context

        logger.info(f"Received action: {action}")
        
        # Tool dispatch
        if action == "example_tool":
            result = example_tool.execute(parameters)
            return MCPResponse(result=result)
        elif action == "knowledge_tool":
            result = knowledge_tool.execute(parameters)
            return MCPResponse(result=result)
        elif action == "list_resources":
            # List all supported MXP resource types
            resources = [
                "account", "crew", "folio", "document", "icafe",
                "person_image", "quick_code", "sailor_manifest",
                "receipt_image", "person_invoice"
            ]
            return MCPResponse(result=resources)
        elif action == "read_resource":
            # Dispatch to correct MXP function based on resource_type using match-case
            resource_type = parameters.get("resource_type")
            if not resource_type:
                raise HTTPException(status_code=400, detail="Missing resource_type parameter")
            try:
                match resource_type:
                    case "account":
                        charge_id = parameters.get("charge_id")
                        if not charge_id:
                            raise HTTPException(status_code=400, detail="Missing charge_id for account")
                        result = get_account(charge_id)
                    case "crew":
                        result = get_crew()
                    case "folio":
                        folio_id = parameters.get("folio_id")
                        if not folio_id:
                            raise HTTPException(status_code=400, detail="Missing folio_id for folio")
                        result = get_folio(folio_id)
                    case "document":
                        document_id = parameters.get("document_id")
                        if not document_id:
                            raise HTTPException(status_code=400, detail="Missing document_id for document")
                        result = get_document(document_id)
                    case "icafe":
                        icafe_id = parameters.get("icafe_id")
                        result = get_icafe(icafe_id)
                    case "person_image":
                        person_id = parameters.get("person_id")
                        if not person_id:
                            raise HTTPException(status_code=400, detail="Missing person_id for person_image")
                        result = get_person_image_by_id(person_id)
                    case "quick_code":
                        result = get_quick_code()
                    case "sailor_manifest":
                        result = get_sailor_manifest()
                    case "receipt_image":
                        receipt_id = parameters.get("receipt_id")
                        if not receipt_id:
                            raise HTTPException(status_code=400, detail="Missing receipt_id for receipt_image")
                        result = get_receipt_image(receipt_id)
                    case "person_invoice":
                        person_id = parameters.get("person_id")
                        if not person_id:
                            raise HTTPException(status_code=400, detail="Missing person_id for person_invoice")
                        result = get_person_invoice(person_id)
                    case _:
                        raise HTTPException(status_code=400, detail=f"Unknown resource_type: {resource_type}")
                return MCPResponse(result=result)
            except Exception as e:
                logger.error(f"MXP resource fetch error: {str(e)}")
                return MCPResponse(result=None, error=str(e))
        else:
            raise HTTPException(status_code=400, detail=f"Unknown action: {action}")
    
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return MCPResponse(result=None, error=str(e))

@app.get("/list-tools")
async def list_tools():
    """
    Return a list of available tools.
    """
    tools = [
        {
            "name": "example_tool",
            "description": "An example tool",
            "parameters": {
                "message": {
                    "type": "string",
                    "description": "A message to echo"
                }
            }
        },
        {
            "name": "knowledge_tool",
            "description": "Access and search knowledge base information",
            "parameters": {
                "operation": {
                    "type": "string",
                    "description": "Operation to perform (search, get, add, delete)"
                },
                "query": {
                    "type": "string",
                    "description": "Search query (for search operation)"
                },
                "tags": {
                    "type": "array",
                    "description": "Tags to filter by (for search operation)"
                },
                "id": {
                    "type": "string",
                    "description": "Entry ID (for get and delete operations)"
                },
                "entry": {
                    "type": "object",
                    "description": "Entry data (for add operation)"
                }
            }
        }
    ]
    return {"tools": tools}

@app.post("/debug")
async def debug_endpoint(request: Request):
    """
    Debug endpoint that echoes back the request body.
    """
    body = await request.json()
    return {"request": body}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=True)
