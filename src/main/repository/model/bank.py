import uuid

from ...db import db


class BankEntity(db.Model):
    """
    A repository model class representing a Bank entity
    """

    __tablename__ = 'banks'

    # automatically generate a unique UUID4 string as the default primary key value
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)

    def __init__(self, name, location):
        self.name = name
        self.location = location
