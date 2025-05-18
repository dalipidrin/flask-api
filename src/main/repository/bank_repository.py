from typing import List, Dict

from .model.bank import BankEntity
from ..db import db


class BankRepository:
    """
    Provides the necessary methods for interacting with the BankEntity in the database.
    """

    @staticmethod
    def create_bank(bank_entity: BankEntity):
        """
        Persists a new BankEntity to the database.

        :param bank_entity: The BankEntity object to be created.
        :return: None.
        """

        db.session.add(bank_entity)
        db.session.commit()

    @staticmethod
    def get_all_banks() -> List[BankEntity]:
        """
        Retrieves all BankEntity objects from the database.

        :return: A list containing all BankEntity objects.
        """

        return BankEntity.query.all()

    @staticmethod
    def update_bank(bank_id: str, data: Dict) -> BankEntity:
        """
        Updates an existing BankEntity in the database.

        :param bank_id: The unique identifier of the bank to be updated.
        :param data: A dictionary containing the data to be updated for the bank.
        :return: The updated BankEntity object.
        :raise Exception: If bank is not found.
        """

        bank_to_update = BankEntity.query.filter_by(id=bank_id).first()
        if not bank_to_update:
            raise Exception("Bank not found")

        # update fields based on given data
        bank_to_update.name = data['name']
        bank_to_update.location = data['location']

        # save and return the updated BankEntity
        db.session.commit()
        return bank_to_update

    @staticmethod
    def delete_bank(bank_id: int) -> bool:
        """
        Deletes a BankEntity object from the database based on the given bank id.

        :param bank_id: The unique identifier of the bank to be deleted.
        :return: True if the bank was successfully deleted, False otherwise (if not found).
        """

        bank = BankEntity.query.get(bank_id)
        if not bank:
            return False

        db.session.delete(bank)
        db.session.commit()
        return True

    @staticmethod
    def get_bank_by_id(bank_id: str) -> BankEntity:
        """
        Retrieves a specific BankEntity from the database based on the given bank id.

        :param bank_id: The unique identifier of the bank to be retrieved.
        :return: The BankEntity object with the matching bank id, or None if not found.
        """

        return BankEntity.query.filter_by(id=bank_id).first()
