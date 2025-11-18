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

MXP_BASE_URL = os.getenv("MXP_BASE_URL", "http://localhost/api")
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


def get_crew() -> dict[str, Any]:
    """
    Get crew information.

    Returns:
        Crew information from MXP system
    """
    url = f"{MXP_BASE_URL}/crew"
    response = requests.get(url, auth=HTTPBasicAuth(MXP_USERNAME, MXP_PASSWORD))
    response.raise_for_status()
    return response.json()


def get_folio(folio_id: int) -> dict[str, Any]:
    """
    Get folio information by folio ID.

    Args:
        folio_id: The folio ID to look up

    Returns:
        Folio information from MXP system
    """
    url = f"{MXP_BASE_URL}/folio"
    params = {"folio_id": folio_id}
    response = requests.get(
        url, params=params, auth=HTTPBasicAuth(MXP_USERNAME, MXP_PASSWORD)
    )
    response.raise_for_status()
    return response.json()


def get_document(document_id: int) -> dict[str, Any]:
    """
    Get document information by document ID.

    Args:
        document_id: The document ID to look up

    Returns:
        Document information from MXP system
    """
    url = f"{MXP_BASE_URL}/document"
    params = {"document_id": document_id}
    response = requests.get(
        url, params=params, auth=HTTPBasicAuth(MXP_USERNAME, MXP_PASSWORD)
    )
    response.raise_for_status()
    return response.json()


def get_icafe(icafe_id: int | None = None) -> dict[str, Any]:
    """
    Get iCafe information, optionally filtered by icafe_id.

    Args:
        icafe_id: Optional iCafe ID to filter by

    Returns:
        iCafe information from MXP system
    """
    url = f"{MXP_BASE_URL}/iCafe"
    params = {"icafe_id": icafe_id} if icafe_id is not None else None
    response = requests.get(
        url, params=params, auth=HTTPBasicAuth(MXP_USERNAME, MXP_PASSWORD)
    )
    response.raise_for_status()
    return response.json()


def get_person_image_by_id(person_id: int) -> dict[str, Any]:
    """
    Get person image by person ID.

    Args:
        person_id: The person ID to look up

    Returns:
        Person image information from MXP system
    """
    url = f"{MXP_BASE_URL}/personImageById"
    params = {"person_id": person_id}
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


def get_sailor_manifest() -> dict[str, Any]:
    """
    Get sailor manifest information.

    Returns:
        Sailor manifest information from MXP system
    """
    url = f"{MXP_BASE_URL}/sailorManifest"
    response = requests.get(url, auth=HTTPBasicAuth(MXP_USERNAME, MXP_PASSWORD))
    response.raise_for_status()
    return response.json()


def get_receipt_image(receipt_id: int) -> dict[str, Any]:
    """
    Get receipt image by receipt ID.

    Args:
        receipt_id: The receipt ID to look up

    Returns:
        Receipt image information from MXP system
    """
    url = f"{MXP_BASE_URL}/receiptImage"
    params = {"receipt_id": receipt_id}
    response = requests.get(
        url, params=params, auth=HTTPBasicAuth(MXP_USERNAME, MXP_PASSWORD)
    )
    response.raise_for_status()
    return response.json()


def get_person_invoice(person_id: int) -> dict[str, Any]:
    """
    Get person invoice by person ID.

    Args:
        person_id: The person ID to look up

    Returns:
        Person invoice information from MXP system
    """
    url = f"{MXP_BASE_URL}/personInvoice"
    params = {"person_id": person_id}
    response = requests.get(
        url, params=params, auth=HTTPBasicAuth(MXP_USERNAME, MXP_PASSWORD)
    )
    response.raise_for_status()
    return response.json()
