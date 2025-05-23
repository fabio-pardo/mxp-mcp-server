#!/usr/bin/env python3
"""
Virgin Voyages MXP API Server
A simple REST API server for accessing MXP endpoints.

Each MXP API function is exposed as a dedicated endpoint.
"""

import logging
import os
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi_mcp.server import FastApiMCP

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

# MXP API endpoints

@app.get("/account/{charge_id}", tags=["MXP"])
async def account(charge_id: int):
    """Get account information by charge ID"""
    try:
        result = get_account(charge_id)
        return result
    except Exception as e:
        logger.error(f"Error getting account: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/crew", tags=["MXP"])
async def crew():
    """Get crew information"""
    try:
        result = get_crew()
        return result
    except Exception as e:
        logger.error(f"Error getting crew: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/folio/{folio_id}", tags=["MXP"])
async def folio(folio_id: int):
    """Get folio information by folio ID"""
    try:
        result = get_folio(folio_id)
        return result
    except Exception as e:
        logger.error(f"Error getting folio: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/document/{document_id}", tags=["MXP"])
async def document(document_id: int):
    """Get document information by document ID"""
    try:
        result = get_document(document_id)
        return result
    except Exception as e:
        logger.error(f"Error getting document: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/icafe", tags=["MXP"])
async def icafe(icafe_id: Optional[int] = None):
    """Get iCafe information, optionally filtered by iCafe ID"""
    try:
        result = get_icafe(icafe_id)
        return result
    except Exception as e:
        logger.error(f"Error getting iCafe: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/person-image/{person_id}", tags=["MXP"])
async def person_image(person_id: int):
    """Get person image by person ID"""
    try:
        result = get_person_image_by_id(person_id)
        return result
    except Exception as e:
        logger.error(f"Error getting person image: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/quick-code", tags=["MXP"])
async def quick_code():
    """Get quick code information"""
    try:
        result = get_quick_code()
        return result
    except Exception as e:
        logger.error(f"Error getting quick code: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/sailor-manifest", tags=["MXP"])
async def sailor_manifest():
    """Get sailor manifest information"""
    try:
        result = get_sailor_manifest()
        return result
    except Exception as e:
        logger.error(f"Error getting sailor manifest: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/receipt-image/{receipt_id}", tags=["MXP"])
async def receipt_image(receipt_id: int):
    """Get receipt image by receipt ID"""
    try:
        result = get_receipt_image(receipt_id)
        return result
    except Exception as e:
        logger.error(f"Error getting receipt image: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/person-invoice/{person_id}", tags=["MXP"])
async def person_invoice(person_id: int):
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
