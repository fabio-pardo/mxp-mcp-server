#!/usr/bin/env python3
"""
Virgin Voyages MXP REST API Server.

This is a traditional REST API server that provides HTTP endpoints for accessing
the Virgin Voyages MXP system. This server maintains backward compatibility with
existing REST API clients.
"""

import logging
import os
import sys
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Import MXP client functions
# Add the parent directory to the path to enable imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from shared.mxp_client import (
    get_account,
    get_crew,
    get_document,
    get_folio,
    get_icafe,
    get_person_image_by_id,
    get_person_invoice,
    get_quick_code,
    get_receipt_image,
    get_sailor_manifest,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Virgin Voyages MXP REST API",
    description="REST API for accessing Virgin Voyages MXP system",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =============================================================================
# Health Check Endpoints
# =============================================================================


@app.get("/", summary="Root endpoint", tags=["Health"])
async def root() -> dict[str, str]:
    """Root endpoint. Returns server running status."""
    return {"message": "MXP REST API Server is running"}


@app.get("/healthz", summary="Health check", tags=["Health"])
async def health_check() -> dict[str, str]:
    """Health check endpoint. Returns OK if server is healthy."""
    return {"status": "healthy"}


# =============================================================================
# MXP API Endpoints
# =============================================================================


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
async def crew(pin: int | None = None) -> dict[str, Any]:
    """Get crew information, optionally filtered by PIN"""
    try:
        result = get_crew(pin)
        return result
    except Exception as e:
        logger.error(f"Error getting crew: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/folio/{charge_id}", tags=["MXP"])
async def folio(
    charge_id: int, date_from: str | None = None, date_to: str | None = None
) -> dict[str, Any]:
    """Get folio information by charge ID with optional date filters"""
    try:
        result = get_folio(charge_id, date_from, date_to)
        return result
    except Exception as e:
        logger.error(f"Error getting folio: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/document/{id}", tags=["MXP"])
async def document(id: str) -> dict[str, Any]:
    """Get document information by document ID (GUID)"""
    try:
        result = get_document(id)
        return result
    except Exception as e:
        logger.error(f"Error getting document: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/icafe", tags=["MXP"])
async def icafe(
    room_nr: str | None = None,
    date_of_birth: str | None = None,
    last_name: str | None = None,
    pin: int | None = None,
) -> dict[str, Any]:
    """Get iCafe information for guests (room_nr, date_of_birth) or crew (pin, last_name)"""
    try:
        result = get_icafe(room_nr, date_of_birth, last_name, pin)
        return result
    except Exception as e:
        logger.error(f"Error getting iCafe: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/person-image/{id}", tags=["MXP"])
async def person_image(id: int) -> dict[str, Any]:
    """Get person image by person ID"""
    try:
        result = get_person_image_by_id(id)
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
async def sailor_manifest(
    installation_code: str, voyage_embark_date: str, voyage_debark_date: str
) -> dict[str, Any]:
    """Get sailor manifest information"""
    try:
        result = get_sailor_manifest(
            installation_code, voyage_embark_date, voyage_debark_date
        )
        return result
    except Exception as e:
        logger.error(f"Error getting sailor manifest: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/receipt-image/{check_number}/{bu_id}", tags=["MXP"])
async def receipt_image(check_number: int, bu_id: int) -> dict[str, Any]:
    """Get receipt image by check number and business unit ID"""
    try:
        result = get_receipt_image(check_number, bu_id)
        return result
    except Exception as e:
        logger.error(f"Error getting receipt image: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/person-invoice/{charge_id}", tags=["MXP"])
async def person_invoice(charge_id: int) -> dict[str, Any]:
    """Get person invoice by charge ID"""
    try:
        result = get_person_invoice(charge_id)
        return result
    except Exception as e:
        logger.error(f"Error getting person invoice: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8000))
    # Run without reload to avoid module path issues
    # For development with reload, use: PYTHONPATH=. uvicorn src.rest_api.server:app --reload
    uvicorn.run(app, host="0.0.0.0", port=port, reload=False)
