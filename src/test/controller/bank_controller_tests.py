import unittest
from unittest.mock import MagicMock, patch
from flask import Flask
from src.main.controller.bank_controller import bank_controller


class BankControllerTests(unittest.TestCase):
    """
    Unit test class that tests BankController endpoints.

    This test class uses Flask's test client to simulate HTTP requests to the `/api/banks` endpoints and verify that the controller
    correctly interacts with the BankService layer.
    """

    def setUp(self):
        # Set up a Flask test app and patch the `bank_service` used in the controller to allow isolating the controller logic from the
        # actual service and database.
        app = Flask(__name__)
        app.register_blueprint(bank_controller)
        self.app = app
        self.client = app.test_client()
        patcher = patch('src.main.controller.bank_controller.bank_service')
        self.mock_service = patcher.start()

    def test_create_bank(self):
        # given (a mock bank object returned by the service layer)
        mock_bank = MagicMock()
        mock_bank.id = '1'
        mock_bank.name = 'Test Bank'
        mock_bank.location = 'Test Location'
        self.mock_service.create_bank.return_value = mock_bank

        # when (a POST request is made to `/api/banks` endpoint with correct json data)
        response = self.client.post('/api/banks', json={
            "name": "Test Bank",
            "location": "Test Location"
        })

        # then (a 200 response with a message indicating that a bank was successfully created)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["message"], "Bank created successfully")

    def test_create_bank_with_missing_required_fields_that_bad_request(self):
        # given / when (a POST request is made to `/api/banks` endpoint with a missing field 'name')
        response_missing_name = self.client.post('/api/banks', json={
            "location": "City X"
        })

        # then (a 400 Bad Request is returned with the message indicating that a required field is missing)
        self.assertEqual(response_missing_name.status_code, 400)
        self.assertEqual(response_missing_name.get_json()["error"], "Both 'name' and 'location' fields are required.")

        # given / when (a POST request is made to `/api/banks` endpoint with a missing field 'location')
        response_missing_location = self.client.post('/api/banks', json={
            "name": "Bank X"
        })

        # then (a 400 Bad Request is returned with the message indicating that a required field is missing)
        self.assertEqual(response_missing_location.status_code, 400)
        self.assertEqual(response_missing_location.get_json()["error"], "Both 'name' and 'location' fields are required.")

        # given / when (a POST request is made to `/api/banks` endpoint with missing both fields 'name' and 'location')
        response_missing_both = self.client.post('/api/banks', json={})

        # then (a 400 Bad Request is returned with the message indicating that a required field is missing)
        self.assertEqual(response_missing_both.status_code, 400)
        self.assertEqual(response_missing_both.get_json()["error"], "Both 'name' and 'location' fields are required.")

    def test_get_all_banks(self):
        # given (2 mock banks returned from the service)
        mock_bank_1 = MagicMock()
        mock_bank_1.dict.return_value = {"id": "1", "name": "Bank A", "location": "City A"}
        mock_bank_2 = MagicMock()
        mock_bank_2.dict.return_value = {"id": "2", "name": "Bank B", "location": "City B"}
        self.mock_service.list_banks.return_value = [mock_bank_1, mock_bank_2]

        # when (a GET request is made to `/api/banks` endpoint)
        response = self.client.get('/api/banks')

        # then (a 200 response is returned with the list of banks)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertEqual(data[0]["name"], "Bank A")
        self.assertEqual(data[0]["location"], "City A")
        self.assertEqual(data[1]["name"], "Bank B")
        self.assertEqual(data[1]["location"], "City B")

    def test_update_bank_that_success(self):
        # given (1 mock bank returned from the service)
        mock_bank = MagicMock()
        mock_bank.dict.return_value = {"id": "1", "name": "Updated Bank", "location": "Updated City"}
        self.mock_service.update_bank.return_value = mock_bank

        # when (a PUT request is made to `/api/banks/{id}` endpoint)
        response = self.client.put('/api/banks/1', json={
            "name": "Updated Bank",
            "location": "Updated City"
        })

        # then (a 200 response is returned with the data of the updated bank)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["name"], "Updated Bank")
        self.assertEqual(data["location"], "Updated City")

    def test_update_that_bank_not_found(self):
        # given (an exception is thrown in the service)
        self.mock_service.update_bank.side_effect = Exception("Bank not found")

        # when (a PUT request is made to `/api/banks/{id}` endpoint)
        response = self.client.put('/api/banks/1', json={
            "name": "X",
            "location": "Y"
        })

        # then (a 400 Bad request is returned)
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data["error"], "Bank not found")

    def test_delete_bank_that_success(self):
        # given (the bank service returns True indicating the bank was successfully deleted)
        self.mock_service.delete_bank.return_value = True

        # when (a DELETE request is made to `/banks/{id}` endpoint)
        response = self.client.delete('/api/banks/1')

        # then (a 200 response is returned with the message confirming successful deletion)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["message"], "Bank deleted successfully")

    def test_delete_bank_that_not_found(self):
        # given (the bank service returns False indicating the bank was successfully deleted)
        self.mock_service.delete_bank.return_value = False

        # when (a DELETE request is made to `/banks/{id}` endpoint)
        response = self.client.delete('/api/banks/1')

        # then (a 404 response is returned with the message indicating that the bank was not found)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json()["message"], "Bank not found")

    def test_get_bank_details_that_success(self):
        # given (a mock bank object returned by the service layer)
        mock_bank = MagicMock()
        mock_bank.dict.return_value = {"id": "1", "name": "Bank A", "location": "City A"}
        self.mock_service.get_bank.return_value = mock_bank

        # when (a GET request is made to `/banks/{id}` endpoint)
        response = self.client.get('/api/banks/1')

        # then (a 200 response is returned with the data of the requested bank)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["name"], "Bank A")
        self.assertEqual(data["location"], "City A")

    def test_get_bank_details_that_not_found(self):
        # given (a mock bank object returned by the service layer)
        self.mock_service.get_bank.return_value = None

        # when (a GET request is made to `/banks/{id}` endpoint)
        response = self.client.get('/api/banks/1')

        # then (a 404 Not Found response is returned with the message indicating that bank was not found)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json()["message"], "Bank not found")


if __name__ == '__main__':
    unittest.main()
