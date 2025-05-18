import os
from dotenv import load_dotenv

load_dotenv()


class DbConfig:
    """
    Configuration class which reads the database connection environment variables from `.env`.
    """

    DB_SERVER = os.getenv('DB_SERVER')
    DB_NAME = os.getenv('DB_NAME')
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_DRIVER = os.getenv('DB_DRIVER').replace(' ', '+')

    SQLALCHEMY_DATABASE_URI = (
        f"mssql+pyodbc://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}/{DB_NAME}"
        f"?driver={DB_DRIVER}&TrustServerCertificate=yes"
    )
