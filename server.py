#!/usr/bin/env python3
"""
Virgin Voyages MXP API Server
A simple REST API server for accessing MXP endpoints.

Each MXP API function is exposed as a dedicated endpoint.
"""

import logging
import os
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi_mcp.server import FastApiMCP  # type: ignore[import-untyped]
from pydantic import BaseModel

# Import MXP API functions
from mxp_api import (
    get_account,
    get_crew,
    get_folio,
    get_document,
    get_icafe,
    get_person_image_by_id,
    get_quick_code,
    get_sailor_manifest,
    get_receipt_image,
    get_person_invoice,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


# Pydantic models for MCP requests
class MCPRequest(BaseModel):
    action: str
    parameters: dict[str, Any] = {}


# Create FastAPI app
app = FastAPI(title="Virgin Voyages MXP API Server")
mcp = FastApiMCP(app)
mcp.mount()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoints
@app.get("/", summary="Root endpoint", tags=["Health"])
async def root():
    """Root endpoint. Returns server running status."""
    return {"message": "MXP API Server is running"}


@app.get("/healthz", summary="Health check", tags=["Health"])
async def health_check():
    """Health check endpoint. Returns OK if server is healthy."""
    return {"status": "healthy"}


# MCP endpoint
@app.post("/mcp", tags=["MCP"])
async def mcp_endpoint(request: MCPRequest):
    """
    Main MCP endpoint for handling various actions.

    Supported actions:
    - list_resources: List all available MXP resources
    - read_resource: Read a specific MXP resource (requires resource_type and ID)
    """
    try:
        action = request.action
        params = request.parameters

        if action == "list_resources":
            # Return list of available resources
            return {
                "result": {
                    "resources": [
                        {
                            "type": "account",
                            "description": "Account information by charge ID",
                        },
                        {"type": "crew", "description": "Crew information"},
                        {
                            "type": "folio",
                            "description": "Folio information by folio ID",
                        },
                        {
                            "type": "document",
                            "description": "Document information by document ID",
                        },
                        {"type": "icafe", "description": "iCafe information"},
                        {
                            "type": "person_image",
                            "description": "Person image by person ID",
                        },
                        {"type": "quick_code", "description": "Quick code information"},
                        {
                            "type": "sailor_manifest",
                            "description": "Sailor manifest information",
                        },
                        {
                            "type": "receipt_image",
                            "description": "Receipt image by receipt ID",
                        },
                        {
                            "type": "person_invoice",
                            "description": "Person invoice by person ID",
                        },
                    ]
                },
                "error": None,
                "metadata": None,
            }

        elif action == "read_resource":
            resource_type = params.get("resource_type")

            if resource_type == "account":
                charge_id = params.get("charge_id")
                if not charge_id or not isinstance(charge_id, int):
                    raise HTTPException(
                        status_code=400,
                        detail="charge_id is required for account resource and must be an integer",
                    )
                result = get_account(int(charge_id))

            elif resource_type == "crew":
                result = get_crew()

            elif resource_type == "folio":
                folio_id = params.get("folio_id")
                if not folio_id or not isinstance(folio_id, int):
                    raise HTTPException(
                        status_code=400,
                        detail="folio_id is required for folio resource and must be an integer",
                    )
                result = get_folio(int(folio_id))

            elif resource_type == "document":
                document_id = params.get("document_id")
                if not document_id or not isinstance(document_id, int):
                    raise HTTPException(
                        status_code=400,
                        detail="document_id is required for document resource and must be an integer",
                    )
                result = get_document(int(document_id))

            elif resource_type == "icafe":
                icafe_id = params.get("icafe_id")
                result = get_icafe(
                    int(icafe_id) if icafe_id and isinstance(icafe_id, int) else None
                )

            elif resource_type == "person_image":
                person_id = params.get("person_id")
                if not person_id or not isinstance(person_id, int):
                    raise HTTPException(
                        status_code=400,
                        detail="person_id is required for person_image resource and must be an integer",
                    )
                result = get_person_image_by_id(int(person_id))

            elif resource_type == "quick_code":
                result = get_quick_code()

            elif resource_type == "sailor_manifest":
                result = get_sailor_manifest()

            elif resource_type == "receipt_image":
                receipt_id = params.get("receipt_id")
                if not receipt_id or not isinstance(receipt_id, int):
                    raise HTTPException(
                        status_code=400,
                        detail="receipt_id is required for receipt_image resource and must be an integer",
                    )
                result = get_receipt_image(int(receipt_id))

            elif resource_type == "person_invoice":
                person_id = params.get("person_id")
                if not person_id or not isinstance(person_id, int):
                    raise HTTPException(
                        status_code=400,
                        detail="person_id is required for person_invoice resource and must be an integer",
                    )
                result = get_person_invoice(int(person_id))

            else:
                raise HTTPException(
                    status_code=400, detail=f"Unknown resource_type: {resource_type}"
                )

            return {"result": result, "error": None, "metadata": None}

        else:
            raise HTTPException(status_code=400, detail=f"Unknown action: {action}")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing MCP request: {str(e)}")
        return {"result": None, "error": str(e), "metadata": None}


# MXP API endpoints


@app.get("/account/{charge_id}", tags=["MXP"])
async def account(charge_id: int) -> dict[str, Any]:
    """Get account information by charge ID"""
    try:
        result = get_account(charge_id)
        return result
    except Exception as e:
        logger.error(f"Error getting account: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/crew", tags=["MXP"])
async def crew() -> dict[str, Any]:
    """Get crew information"""
    try:
        result = get_crew()
        return result
    except Exception as e:
        logger.error(f"Error getting crew: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/folio/{folio_id}", tags=["MXP"])
async def folio(folio_id: int) -> dict[str, Any]:
    """Get folio information by folio ID"""
    try:
        result = get_folio(folio_id)
        return result
    except Exception as e:
        logger.error(f"Error getting folio: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/document/{document_id}", tags=["MXP"])
async def document(document_id: int) -> dict[str, Any]:
    """Get document information by document ID"""
    try:
        result = get_document(document_id)
        return result
    except Exception as e:
        logger.error(f"Error getting document: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/icafe", tags=["MXP"])
async def icafe(icafe_id: int | None = None) -> dict[str, Any]:
    """Get iCafe information, optionally filtered by iCafe ID"""
    try:
        result = get_icafe(icafe_id)
        return result
    except Exception as e:
        logger.error(f"Error getting iCafe: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/person-image/{person_id}", tags=["MXP"])
async def person_image(person_id: int) -> dict[str, Any]:
    """Get person image by person ID"""
    try:
        result = get_person_image_by_id(person_id)
        return result
    except Exception as e:
        logger.error(f"Error getting person image: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/quick-code", tags=["MXP"])
async def quick_code() -> dict[str, Any]:
    """Get quick code information"""
    try:
        result = get_quick_code()
        return result
    except Exception as e:
        logger.error(f"Error getting quick code: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/sailor-manifest", tags=["MXP"])
async def sailor_manifest() -> dict[str, Any]:
    """Get sailor manifest information"""
    try:
        result = get_sailor_manifest()
        return result
    except Exception as e:
        logger.error(f"Error getting sailor manifest: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/receipt-image/{receipt_id}", tags=["MXP"])
async def receipt_image(receipt_id: int) -> dict[str, Any]:
    """Get receipt image by receipt ID"""
    try:
        result = get_receipt_image(receipt_id)
        return result
    except Exception as e:
        logger.error(f"Error getting receipt image: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/person-invoice/{person_id}", tags=["MXP"])
async def person_invoice(person_id: int) -> dict[str, Any]:
    """Get person invoice by person ID"""
    try:
        result = get_person_invoice(person_id)
        return result
    except Exception as e:
        logger.error(f"Error getting person invoice: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


mcp.setup_server()

if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=True)
