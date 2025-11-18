"""
Virgin Voyages MXP API Client.

This module provides a Python client for interacting with the Virgin Voyages MXP system.
All functions communicate with the MXP backend using HTTP Basic Authentication.
"""

import os
from typing import Any

import requests
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

# Load environment variables from .env file
_ = load_dotenv()

MXP_BASE_URL = os.getenv("MXP_BASE_URL", "http://localhost/MXP_Virgin.exe")
MXP_USERNAME = os.getenv("MXP_USERNAME", "username")
MXP_PASSWORD = os.getenv("MXP_PASSWORD", "password")


def get_account(charge_id: int) -> dict[str, Any]:
    """
    Get account information by charge ID.

    Args:
        charge_id: The charge ID to look up

    Returns:
        Account information from MXP system
    """
    url = f"{MXP_BASE_URL}/account"
    params = {"charge_id": charge_id}
    response = requests.get(
        url, params=params, auth=HTTPBasicAuth(MXP_USERNAME, MXP_PASSWORD)
    )
    response.raise_for_status()
    return response.json()


def get_crew(pin: int | None = None) -> dict[str, Any]:
    """
    Get crew information, optionally filtered by PIN.

    Args:
        pin: Optional PIN to filter by specific crew member

    Returns:
        Crew information from MXP system
    """
    url = f"{MXP_BASE_URL}/crew"
    params = {"PIN": pin} if pin is not None else None
    response = requests.get(
        url, params=params, auth=HTTPBasicAuth(MXP_USERNAME, MXP_PASSWORD)
    )
    response.raise_for_status()
    return response.json()


def get_folio(
    charge_id: int, date_from: str | None = None, date_to: str | None = None
) -> dict[str, Any]:
    """
    Get folio information by charge ID with optional date filters.

    Args:
        charge_id: The charge ID to look up
        date_from: Optional start date (ISO 8601 format: YYYY-MM-DD)
        date_to: Optional end date (ISO 8601 format: YYYY-MM-DD)

    Returns:
        Folio information from MXP system
    """
    url = f"{MXP_BASE_URL}/folio"
    params: dict[str, Any] = {"charge_id": charge_id}
    if date_from:
        params["date_from"] = date_from
    if date_to:
        params["date_to"] = date_to
    response = requests.get(
        url, params=params, auth=HTTPBasicAuth(MXP_USERNAME, MXP_PASSWORD)
    )
    response.raise_for_status()
    return response.json()


def get_document(id: str) -> dict[str, Any]:
    """
    Get document information by document ID (GUID).

    Args:
        id: The document GUID to look up

    Returns:
        Document information from MXP system
    """
    url = f"{MXP_BASE_URL}/document"
    params = {"id": id}
    response = requests.get(
        url, params=params, auth=HTTPBasicAuth(MXP_USERNAME, MXP_PASSWORD)
    )
    response.raise_for_status()
    return response.json()


def get_icafe(
    room_nr: str | None = None,
    date_of_birth: str | None = None,
    last_name: str | None = None,
    pin: int | None = None,
) -> dict[str, Any]:
    """
    Get iCafe package information.

    For guests, use room_nr and date_of_birth.
    For crew, use pin and last_name.

    Args:
        room_nr: Room number (for guests)
        date_of_birth: Date of birth in ISO 8601 format (for guests)
        last_name: Last name (for crew)
        pin: Person ID (for crew)

    Returns:
        iCafe information from MXP system
    """
    url = f"{MXP_BASE_URL}/iCafe"
    params: dict[str, Any] = {}
    if room_nr:
        params["room_nr"] = room_nr
    if date_of_birth:
        params["date_of_birth"] = date_of_birth
    if last_name:
        params["last_name"] = last_name
    if pin is not None:
        params["pin"] = pin

    response = requests.get(
        url,
        params=params if params else None,
        auth=HTTPBasicAuth(MXP_USERNAME, MXP_PASSWORD),
    )
    response.raise_for_status()
    return response.json()


def get_person_image_by_id(id: int) -> dict[str, Any]:
    """
    Get person image by person ID.

    Args:
        id: The MXP internal person identifier

    Returns:
        Person image information from MXP system
    """
    url = f"{MXP_BASE_URL}/personImageById"
    params = {"id": id}
    response = requests.get(
        url, params=params, auth=HTTPBasicAuth(MXP_USERNAME, MXP_PASSWORD)
    )
    response.raise_for_status()
    return response.json()


def get_quick_code() -> dict[str, Any]:
    """
    Get quick code information.

    Returns:
        Quick code information from MXP system
    """
    url = f"{MXP_BASE_URL}/quickCode"
    response = requests.get(url, auth=HTTPBasicAuth(MXP_USERNAME, MXP_PASSWORD))
    response.raise_for_status()
    return response.json()


def get_sailor_manifest(
    installation_code: str, voyage_embark_date: str, voyage_debark_date: str
) -> dict[str, Any]:
    """
    Get sailor manifest information.

    Args:
        installation_code: Ship/installation code
        voyage_embark_date: Voyage embark date (ISO 8601 format: YYYY-MM-DD)
        voyage_debark_date: Voyage debark date (ISO 8601 format: YYYY-MM-DD)

    Returns:
        Sailor manifest information from MXP system
    """
    url = f"{MXP_BASE_URL}/sailorManifest"
    params = {
        "installation_code": installation_code,
        "voyage_embark_date": voyage_embark_date,
        "voyage_debark_date": voyage_debark_date,
    }
    response = requests.get(
        url, params=params, auth=HTTPBasicAuth(MXP_USERNAME, MXP_PASSWORD)
    )
    response.raise_for_status()
    return response.json()


def get_receipt_image(check_number: int, bu_id: int) -> dict[str, Any]:
    """
    Get receipt image by check number and business unit ID.

    Args:
        check_number: The check number to look up
        bu_id: Business unit identifier

    Returns:
        Receipt image information from MXP system
    """
    url = f"{MXP_BASE_URL}/receiptImage"
    params = {"check_number": check_number, "bu_id": bu_id}
    response = requests.get(
        url, params=params, auth=HTTPBasicAuth(MXP_USERNAME, MXP_PASSWORD)
    )
    response.raise_for_status()
    return response.json()


def get_person_invoice(charge_id: int) -> dict[str, Any]:
    """
    Get person invoice by charge ID.

    Args:
        charge_id: The charge ID to look up

    Returns:
        Person invoice PDF from MXP system
    """
    url = f"{MXP_BASE_URL}/personInvoice"
    params = {"charge_id": charge_id}
    response = requests.get(
        url, params=params, auth=HTTPBasicAuth(MXP_USERNAME, MXP_PASSWORD)
    )
    response.raise_for_status()
    return response.json()
