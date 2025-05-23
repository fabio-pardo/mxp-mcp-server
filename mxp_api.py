import requests
from requests.auth import HTTPBasicAuth

MXP_BASE_URL = os.getenv("MXP_BASE_URL", "http://localhost/api")
MXP_USERNAME = os.getenv("MXP_USERNAME", "username")
MXP_PASSWORD = os.getenv("MXP_PASSWORD", "password")

def get_account(charge_id):
    """Call the MXP /account/GET endpoint with the given charge_id."""
    url = f"{MXP_BASE_URL}/account"
    params = {"charge_id": charge_id}
    response = requests.get(url, params=params, auth=HTTPBasicAuth(MXP_USERNAME, MXP_PASSWORD))
    response.raise_for_status()
    return response.json()

def get_crew():
    """Call the MXP /crew/GET endpoint to retrieve crew information."""
    url = f"{MXP_BASE_URL}/crew"
    response = requests.get(url, auth=HTTPBasicAuth(MXP_USERNAME, MXP_PASSWORD))
    response.raise_for_status()
    return response.json()

def get_folio(folio_id):
    """Call the MXP /folio/GET endpoint with the given folio_id."""
    url = f"{MXP_BASE_URL}/folio"
    params = {"folio_id": folio_id}
    response = requests.get(url, params=params, auth=HTTPBasicAuth(MXP_USERNAME, MXP_PASSWORD))
    response.raise_for_status()
    return response.json()

def get_document(document_id):
    """Call the MXP /document/GET endpoint with the given document_id."""
    url = f"{MXP_BASE_URL}/document"
    params = {"document_id": document_id}
    response = requests.get(url, params=params, auth=HTTPBasicAuth(MXP_USERNAME, MXP_PASSWORD))
    response.raise_for_status()
    return response.json()

def get_icafe(icafe_id=None):
    """Call the MXP /iCafe/GET endpoint. Optionally filter by icafe_id."""
    url = f"{MXP_BASE_URL}/iCafe"
    params = {"icafe_id": icafe_id} if icafe_id is not None else None
    response = requests.get(url, params=params, auth=HTTPBasicAuth(MXP_USERNAME, MXP_PASSWORD))
    response.raise_for_status()
    return response.json()

def get_person_image_by_id(person_id):
    """Call the MXP /personImageById/GET endpoint with the given person_id."""
    url = f"{MXP_BASE_URL}/personImageById"
    params = {"person_id": person_id}
    response = requests.get(url, params=params, auth=HTTPBasicAuth(MXP_USERNAME, MXP_PASSWORD))
    response.raise_for_status()
    return response.json()

def get_quick_code():
    """Call the MXP /quickCode/GET endpoint."""
    url = f"{MXP_BASE_URL}/quickCode"
    response = requests.get(url, auth=HTTPBasicAuth(MXP_USERNAME, MXP_PASSWORD))
    response.raise_for_status()
    return response.json()

def get_sailor_manifest():
    """Call the MXP /sailorManifest/GET endpoint."""
    url = f"{MXP_BASE_URL}/sailorManifest"
    response = requests.get(url, auth=HTTPBasicAuth(MXP_USERNAME, MXP_PASSWORD))
    response.raise_for_status()
    return response.json()

def get_receipt_image(receipt_id):
    """Call the MXP /receiptImage/GET endpoint with the given receipt_id."""
    url = f"{MXP_BASE_URL}/receiptImage"
    params = {"receipt_id": receipt_id}
    response = requests.get(url, params=params, auth=HTTPBasicAuth(MXP_USERNAME, MXP_PASSWORD))
    response.raise_for_status()
    return response.json()

def get_person_invoice(person_id):
    """Call the MXP /personInvoice/GET endpoint with the given person_id."""
    url = f"{MXP_BASE_URL}/personInvoice"
    params = {"person_id": person_id}
    response = requests.get(url, params=params, auth=HTTPBasicAuth(MXP_USERNAME, MXP_PASSWORD))
    response.raise_for_status()
    return response.json()
