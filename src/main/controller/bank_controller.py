from flask import Blueprint, request, jsonify

from ..repository.bank_repository import BankRepository
from ..service.bank_service import BankService
from ..service.model.bank import Bank

bank_controller = Blueprint('bank_controller', __name__)
bank_repository = BankRepository()
bank_service = BankService(bank_repository)


@bank_controller.route('/', methods=['POST'])
def create_bank():
    """
    Exposed as: /api/banks

    Creates a bank with the given data in the payload. The input must include the `name` and `location` of the bank. Once created, the new
    bank is persisted and its data is returned in the response.

    :return: A JSON response containing a message indicating that a bank was successfully created.
    """

    # validate required fields
    bank_data = request.json
    if not bank_data or "name" not in bank_data or "location" not in bank_data:
        return jsonify({"error": "Both 'name' and 'location' fields are required."}), 400

    # instantiate a Bank model using the data received in the request payload and persist it
    bank = Bank(**bank_data)
    bank_service.create_bank(bank)

    return jsonify({"message": "Bank created successfully"}), 200


@bank_controller.route('/', methods=['GET'])
def get_banks():
    """
    Exposed as: /api/banks

    Retrieves a list of all banks.

    :return: A JSON response containing a list of banks where each bank includes its ID, name, and location
    """

    banks = bank_service.list_banks()
    return jsonify([bank.dict() for bank in banks])


@bank_controller.route('/<bank_id>', methods=['PUT'])
def update_bank(bank_id):
    """
    Exposed as: /api/banks/<bank_id>

    Updates the data of a specific bank based on the given <bank_id> and the data in the payload.

    :param bank_id: The unique identifier of the bank to be updated.
    :return:
        - HTTP 200 OK with a JSON object representing the updated bank if the update is successful
        - HTTP 400 Bad Request with an error message if the update fails due to invalid input or if the bank does not exist
    """

    data = request.json
    try:
        updated_bank = bank_service.update_bank(bank_id, data)
        return jsonify(updated_bank.dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@bank_controller.route('/<bank_id>', methods=['DELETE'])
def delete_bank(bank_id):
    """
    Exposed as: /api/banks/<bank_id>

    Deletes a specific bank based on the given <bank_id>.

    :param bank_id: The unique identifier of the bank to be deleted.
    :return:
        - HTTP 200 OK with a message indicating that delete is successful
        - HTTP 404 Not Found with an error message indicating that the bank to be deleted was not found
    """

    is_bank_deleted = bank_service.delete_bank(bank_id)
    if is_bank_deleted:
        return jsonify({'message': 'Bank deleted successfully'}), 200
    else:
        return jsonify({'message': 'Bank not found'}), 404


@bank_controller.route('/<bank_id>', methods=['GET'])
def get_bank(bank_id):
    """
    Exposed as: /api/banks/<bank_id>

    Retrieves the data of a specific bank based on the given <bank_id>.

    :param bank_id: The unique identifier of the bank to be retrieved.
    :return:
        - HTTP 200 OK with a JSON object containing the details of the requested bank.
        - HTTP 404 Not Found with an error message indicating that the bank requested was not found
    """

    bank = bank_service.get_bank(bank_id)
    if not bank:
        return jsonify({'message': 'Bank not found'}), 404
    return jsonify(bank.dict())
