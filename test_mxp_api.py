import unittest
from unittest.mock import patch
from mxp_api import get_account, get_crew, get_folio

class TestMXPAPI(unittest.TestCase):
    @patch('mxp_api.requests.get')
    def test_get_account_success(self, mock_get):
        # Mocked successful response
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "account_nr": 10000002,
            "charge_id": 10000004,
            "account_name": "John, Doe"
        }
        result = get_account(10000004)
        self.assertEqual(result["account_nr"], 10000002)
        self.assertEqual(result["charge_id"], 10000004)
        self.assertEqual(result["account_name"], "John, Doe")

    @patch('mxp_api.requests.get')
    def test_get_account_error(self, mock_get):
        import requests
        # Mocked error response
        mock_get.return_value.status_code = 400
        mock_get.return_value.json.return_value = {
            "response_code": "INVALID_INPUT_PARAMETERS",
            "response_description": "Missing or wrong parameter {charge_id}"
        }
        mock_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError()
        with self.assertRaises(requests.exceptions.HTTPError):
            get_account(None)

    @patch('mxp_api.requests.get')
    def test_get_crew_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [{"crew_id": 1, "name": "Alice"}]
        result = get_crew()
        self.assertEqual(result[0]["crew_id"], 1)
        self.assertEqual(result[0]["name"], "Alice")

    @patch('mxp_api.requests.get')
    def test_get_crew_error(self, mock_get):
        import requests
        mock_get.return_value.status_code = 500
        mock_get.return_value.json.return_value = {"response_code": "SERVER_ERROR"}
        mock_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError()
        with self.assertRaises(requests.exceptions.HTTPError):
            get_crew()

    @patch('mxp_api.requests.get')
    def test_get_folio_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"folio_id": 123, "charges": []}
        result = get_folio(123)
        self.assertEqual(result["folio_id"], 123)
        self.assertIsInstance(result["charges"], list)

    @patch('mxp_api.requests.get')
    def test_get_folio_error(self, mock_get):
        import requests
        mock_get.return_value.status_code = 404
        mock_get.return_value.json.return_value = {"response_code": "NOT_FOUND"}
        mock_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError()
        with self.assertRaises(requests.exceptions.HTTPError):
            get_folio(999)

if __name__ == "__main__":
    unittest.main()
