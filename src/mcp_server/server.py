#!/usr/bin/env python3
"""
Virgin Voyages MXP-MCP Server.

This is a proper Model Context Protocol (MCP) server that exposes Virgin Voyages MXP
system functionality as tools, resources, and prompts for LLM consumption.

The server supports multiple transports:
- stdio: For Claude Desktop and local MCP clients
- streamable-http: For web-based clients
- sse: For browser-based clients
"""

import os
import sys
from typing import Any, List, Dict

from mcp.server.fastmcp import FastMCP

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
from shared import db_client

# Initialize MCP server
mcp = FastMCP(
    "Virgin Voyages MXP",
    description="MCP server providing access to Virgin Voyages MXP system data",
)


@mcp.tool()
def execute_read_only_query(query: str, params: tuple = ()) -> List[Dict[str, Any]]:
    """
    Executes a read-only SQL SELECT query and returns results as a list of dictionaries.

    Args:
        query: The SQL SELECT query string.
        params: Optional query parameters (use %s placeholders in the query).

    Returns:
        A list of dictionaries, where each dictionary represents a row and
        keys are column names. Returns an empty list if no results are found.
    """
    return db_client.execute_query_dict(query, params)


# =============================================================================
# TOOLS - Functions that LLMs can call
# =============================================================================


@mcp.tool()
def get_account_info(charge_id: int) -> dict[str, Any]:
    """
    Get account information by charge ID from the MXP system.

    Args:
        charge_id: The charge ID to look up (e.g., 10000004)

    Returns:
        Account information including balance, transactions, and details
    """
    return get_account(charge_id)


@mcp.tool()
def get_crew_info(pin: int | None = None) -> dict[str, Any]:
    """
    Get crew information from the MXP system, optionally filtered by PIN.

    Args:
        pin: Optional PIN to filter by specific crew member

    Returns:
        Information about crew members including names, roles, and assignments
    """
    return get_crew(pin)


@mcp.tool()
def get_folio_info(
    charge_id: int, date_from: str | None = None, date_to: str | None = None
) -> dict[str, Any]:
    """
    Get folio information by charge ID from the MXP system.

    Args:
        charge_id: The charge ID to look up
        date_from: Optional start date (ISO 8601 format: YYYY-MM-DD)
        date_to: Optional end date (ISO 8601 format: YYYY-MM-DD)

    Returns:
        Folio information including charges, payments, and balance
    """
    return get_folio(charge_id, date_from, date_to)


@mcp.tool()
def get_document_info(id: str) -> dict[str, Any]:
    """
    Get document information by document ID (GUID) from the MXP system.

    Args:
        id: The document GUID to look up

    Returns:
        Document information including type, status, and content
    """
    return get_document(id)


@mcp.tool()
def get_icafe_info(
    room_nr: str | None = None,
    date_of_birth: str | None = None,
    last_name: str | None = None,
    pin: int | None = None,
) -> dict[str, Any]:
    """
    Get iCafe package information from the MXP system.

    For guests, use room_nr and date_of_birth.
    For crew, use pin and last_name.

    Args:
        room_nr: Room number (for guests)
        date_of_birth: Date of birth in ISO 8601 format (for guests)
        last_name: Last name (for crew)
        pin: Person ID (for crew)

    Returns:
        iCafe package information including usage, time, and location
    """
    return get_icafe(room_nr, date_of_birth, last_name, pin)


@mcp.tool()
def get_person_image(id: int) -> dict[str, Any]:
    """
    Get person image information by person ID from the MXP system.

    Args:
        id: The MXP internal person identifier

    Returns:
        Person image data including URL and metadata
    """
    return get_person_image_by_id(id)


@mcp.tool()
def get_quick_code_info() -> dict[str, Any]:
    """
    Get quick code information from the MXP system.

    Returns:
        Quick code configuration and active codes
    """
    return get_quick_code()


@mcp.tool()
def get_manifest_info(
    installation_code: str, voyage_embark_date: str, voyage_debark_date: str
) -> dict[str, Any]:
    """
    Get sailor manifest information from the MXP system.

    Args:
        installation_code: Ship/installation code
        voyage_embark_date: Voyage embark date (ISO 8601 format: YYYY-MM-DD)
        voyage_debark_date: Voyage debark date (ISO 8601 format: YYYY-MM-DD)

    Returns:
        Sailor manifest including passenger lists and cabin assignments
    """
    return get_sailor_manifest(
        installation_code, voyage_embark_date, voyage_debark_date
    )


@mcp.tool()
def get_receipt_image_info(check_number: int, bu_id: int) -> dict[str, Any]:
    """
    Get receipt image information by check number and business unit ID from the MXP system.

    Args:
        check_number: The check number to look up
        bu_id: Business unit identifier

    Returns:
        Receipt image data including URL and transaction details
    """
    return get_receipt_image(check_number, bu_id)


@mcp.tool()
def get_person_invoice_info(charge_id: int) -> dict[str, Any]:
    """
    Get person invoice information by charge ID from the MXP system.

    Args:
        charge_id: The charge ID to look up

    Returns:
        Person invoice PDF including charges, payments, and balance
    """
    return get_person_invoice(charge_id)


# =============================================================================
# RESOURCES - Data that LLMs can read
# =============================================================================


@mcp.resource("mxp://config/info")
def get_mxp_config() -> str:
    """Expose MXP system configuration information."""
    return """
    Virgin Voyages MXP System Configuration
    
    Available Tools:
    - get_account_info: Retrieve account information by charge ID
    - get_crew_info: Get crew member information
    - get_folio_info: Access folio details
    - get_document_info: Retrieve document information
    - get_icafe_info: Get iCafe session data
    - get_person_image: Access person images
    - get_quick_code_info: Get quick codes
    - get_manifest_info: Access sailor manifest
    - get_receipt_image_info: Get receipt images
    - get_person_invoice_info: Access person invoices
    
    System Status: Active
    """


@mcp.resource("mxp://help/tools")
def get_tool_help() -> str:
    """Provide help information about available tools."""
    return """
    MXP Tool Usage Guide
    
    Account Information:
    - Use get_account_info(charge_id) to retrieve account details
    - Example: get_account_info(10000004)
    
    Folio Information:
    - Use get_folio_info(charge_id, date_from, date_to) to access folio data
    - Folios contain charge and payment information
    - Example: get_folio_info(10000004, "2024-01-01", "2024-01-31")
    
    Document Access:
    - Use get_document_info(id) to retrieve documents by GUID
    - Documents include receipts, confirmations, etc.
    - Example: get_document_info("82056F48-D00B-40AB-9D18-029E1FA67EFF")
    
    Personnel Information:
    - get_crew_info(pin) for crew member data (optional PIN filter)
    - get_person_image(id) for person photos by person ID
    - get_person_invoice_info(charge_id) for invoices by charge ID
    
    Passenger Services:
    - get_icafe_info(room_nr, date_of_birth, last_name, pin) for internet cafe packages
      * For guests: use room_nr and date_of_birth
      * For crew: use pin and last_name
    - get_manifest_info(installation_code, voyage_embark_date, voyage_debark_date)
      for passenger manifests
    - get_quick_code_info() for quick access codes
    - get_receipt_image_info(check_number, bu_id) for receipt images
    """


# =============================================================================
# PROMPTS - Templates for LLM interactions
# =============================================================================


@mcp.prompt()
def analyze_account(charge_id: int) -> str:
    """Generate a prompt to analyze an account."""
    return f"""
    Please analyze the account with charge ID {charge_id}.
    
    Use the get_account_info tool to retrieve the account details, then provide:
    1. Account status summary
    2. Outstanding balance (if any)
    3. Recent transaction patterns
    4. Any potential issues or concerns
    5. Recommendations for account management
    """


@mcp.prompt()
def review_folio(charge_id: int) -> str:
    """Generate a prompt to review a folio."""
    return f"""
    Please review the folio for charge ID {charge_id}.
    
    Use the get_folio_info tool to retrieve the folio details, then provide:
    1. Total charges breakdown
    2. Payment history
    3. Current balance
    4. Unusual or noteworthy items
    5. Suggestions for the guest
    """


@mcp.prompt()
def crew_report() -> str:
    """Generate a prompt to create a crew report."""
    return """
    Please generate a comprehensive crew report.
    
    Use the get_crew_info tool to retrieve crew data, then provide:
    1. Total crew count by department
    2. Role distribution
    3. Any staffing gaps or concerns
    4. Crew performance highlights
    5. Recommendations for crew management
    """


# =============================================================================
# Server Entry Point
# =============================================================================


def main():
    """Run the MCP server with the appropriate transport."""
    import argparse

    parser = argparse.ArgumentParser(description="Virgin Voyages MXP-MCP Server")
    parser.add_argument(
        "--transport",
        choices=["stdio", "streamable-http", "sse"],
        default="stdio",
        help="Transport protocol to use (default: stdio)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port for HTTP transports (default: 8000)",
    )

    args = parser.parse_args()

    # Run server with selected transport
    if args.transport == "stdio":
        # For Claude Desktop and local clients
        import sys

        print("🚀 MCP Server starting in stdio mode...", file=sys.stderr)
        print("✅ Server ready and listening for MCP requests", file=sys.stderr)
        mcp.run(transport="stdio")
    elif args.transport == "streamable-http":
        # For web-based clients (run with uvicorn)
        print(
            f"Run with: uvicorn src.mcp_server.server:mcp.streamable_http_app --host 0.0.0.0 --port {args.port}"
        )
        mcp.run(transport="streamable-http")
    elif args.transport == "sse":
        # For browser-based clients (run with uvicorn)
        print(
            f"Run with: uvicorn src.mcp_server.server:mcp.sse_app --host 0.0.0.0 --port {args.port}"
        )
        mcp.run(transport="sse")


if __name__ == "__main__":
    main()
