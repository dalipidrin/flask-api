from typing import List, Dict, Optional

from .model.bank import Bank
from ..repository.bank_repository import BankRepository
from ..repository.model.bank import BankEntity
from ..utils import to_dict


class BankService:
    """
    Provides business logic for managing bank data.

    This class acts as an intermediary between the controller and the repository, handling data transformation, validation, and
    orchestration of bank-related operations.
    """

    def __init__(self, bank_repository: BankRepository):
        self.bank_repository = bank_repository

    def create_bank(self, bank: Bank):
        """
        Creates a new bank in the database.

        :param bank: A service Bank model containing the bank's data.
        :return: None.
        """

        # map the Bank service model to a BankEntity repository model and persist it
        bank_entity = BankEntity(**bank.dict())
        self.bank_repository.create_bank(bank_entity)

    def list_banks(self) -> List[Bank]:
        """
        Retrieves all banks from the database.

        :return: A list of Bank service models representing banks.
        """

        bank_entities = self.bank_repository.get_all_banks()
        # map each BankEntity repository model to a Bank service model
        banks = [Bank(**to_dict(entity)) for entity in bank_entities]
        return banks

    def update_bank(self, bank_id: str, data: Dict) -> Bank:
        """
        Updates an existing bank in the database.

        :param bank_id: The unique identifier of the bank to be updated.
        :param data: A dictionary containing the data to be updated for the bank.
        :return: The updated Bank service model.
        """

        updated_bank_entity = self.bank_repository.update_bank(bank_id, data)
        # map the updated BankEntity repository model to a Bank service model
        updated_bank = Bank(**to_dict(updated_bank_entity))
        return updated_bank

    def delete_bank(self, bank_id: int) -> bool:
        """
        Deletes a bank from the database based on the given bank id.

        :param bank_id: The unique identifier of the bank to be deleted.
        :return: True if the bank was successfully deleted, False otherwise (if not found).
        """

        return self.bank_repository.delete_bank(bank_id)

    def get_bank(self, bank_id: str) -> Optional[Bank]:
        """
        Retrieves a specific bank from the database based on the given bank id.

        :param bank_id: The unique identifier of the bank to be retrieved.
        :return: The Bank service model representing the bank, or None if not found.
        """

        bank_entity = self.bank_repository.get_bank_by_id(bank_id)
        if not bank_entity:
            return None

        # map the retrieved BankEntity repository model to a Bank service model
        bank = Bank(**to_dict(bank_entity))
        return bank
