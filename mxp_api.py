import requests
from requests.auth import HTTPBasicAuth

MXP_BASE_URL = "http://10.2.225.226/MXP_Virgin.exe"
MXP_USERNAME = "MXP-API-User"
MXP_PASSWORD = "!veryS4f3"

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
