import unittest
from unittest.mock import patch
from mxp_api import (
    get_account, get_crew, get_folio, get_document, get_icafe,
    get_person_image_by_id, get_quick_code, get_sailor_manifest,
    get_receipt_image, get_person_invoice
)

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

    @patch('mxp_api.requests.get')
    def test_get_document_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"document_id": 42, "title": "Test Doc"}
        result = get_document(42)
        self.assertEqual(result["document_id"], 42)
        self.assertEqual(result["title"], "Test Doc")

    @patch('mxp_api.requests.get')
    def test_get_document_error(self, mock_get):
        import requests
        mock_get.return_value.status_code = 404
        mock_get.return_value.json.return_value = {"response_code": "NOT_FOUND"}
        mock_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError()
        with self.assertRaises(requests.exceptions.HTTPError):
            get_document(999)

    @patch('mxp_api.requests.get')
    def test_get_icafe_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [{"icafe_id": 1, "desc": "Coffee"}]
        result = get_icafe()
        self.assertEqual(result[0]["icafe_id"], 1)
        self.assertEqual(result[0]["desc"], "Coffee")

    @patch('mxp_api.requests.get')
    def test_get_icafe_error(self, mock_get):
        import requests
        mock_get.return_value.status_code = 500
        mock_get.return_value.json.return_value = {"response_code": "SERVER_ERROR"}
        mock_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError()
        with self.assertRaises(requests.exceptions.HTTPError):
            get_icafe()

    @patch('mxp_api.requests.get')
    def test_get_person_image_by_id_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"person_id": 101, "image": "base64string"}
        result = get_person_image_by_id(101)
        self.assertEqual(result["person_id"], 101)
        self.assertIn("image", result)

    @patch('mxp_api.requests.get')
    def test_get_person_image_by_id_error(self, mock_get):
        import requests
        mock_get.return_value.status_code = 404
        mock_get.return_value.json.return_value = {"response_code": "NOT_FOUND"}
        mock_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError()
        with self.assertRaises(requests.exceptions.HTTPError):
            get_person_image_by_id(999)

    @patch('mxp_api.requests.get')
    def test_get_quick_code_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [{"code": "A1", "desc": "Test Code"}]
        result = get_quick_code()
        self.assertEqual(result[0]["code"], "A1")

    @patch('mxp_api.requests.get')
    def test_get_quick_code_error(self, mock_get):
        import requests
        mock_get.return_value.status_code = 500
        mock_get.return_value.json.return_value = {"response_code": "SERVER_ERROR"}
        mock_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError()
        with self.assertRaises(requests.exceptions.HTTPError):
            get_quick_code()

    @patch('mxp_api.requests.get')
    def test_get_sailor_manifest_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [{"sailor_id": 1, "name": "Bob"}]
        result = get_sailor_manifest()
        self.assertEqual(result[0]["sailor_id"], 1)

    @patch('mxp_api.requests.get')
    def test_get_sailor_manifest_error(self, mock_get):
        import requests
        mock_get.return_value.status_code = 500
        mock_get.return_value.json.return_value = {"response_code": "SERVER_ERROR"}
        mock_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError()
        with self.assertRaises(requests.exceptions.HTTPError):
            get_sailor_manifest()

    @patch('mxp_api.requests.get')
    def test_get_receipt_image_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"receipt_id": 77, "image": "base64string"}
        result = get_receipt_image(77)
        self.assertEqual(result["receipt_id"], 77)
        self.assertIn("image", result)

    @patch('mxp_api.requests.get')
    def test_get_receipt_image_error(self, mock_get):
        import requests
        mock_get.return_value.status_code = 404
        mock_get.return_value.json.return_value = {"response_code": "NOT_FOUND"}
        mock_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError()
        with self.assertRaises(requests.exceptions.HTTPError):
            get_receipt_image(999)

    @patch('mxp_api.requests.get')
    def test_get_person_invoice_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"person_id": 202, "invoices": [1,2,3]}
        result = get_person_invoice(202)
        self.assertEqual(result["person_id"], 202)
        self.assertIsInstance(result["invoices"], list)

    @patch('mxp_api.requests.get')
    def test_get_person_invoice_error(self, mock_get):
        import requests
        mock_get.return_value.status_code = 404
        mock_get.return_value.json.return_value = {"response_code": "NOT_FOUND"}
        mock_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError()
        with self.assertRaises(requests.exceptions.HTTPError):
            get_person_invoice(999)

if __name__ == "__main__":
    unittest.main()
