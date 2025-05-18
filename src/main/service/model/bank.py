from pydantic import BaseModel


class Bank(BaseModel):
    """
    A service model class representing a Bank
    """

    name: str
    location: str
