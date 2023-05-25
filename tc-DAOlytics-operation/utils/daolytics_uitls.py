import os
from dotenv import load_dotenv


def get_rabbit_mq_credentials() -> dict[str, any]:
    """
    returns the rabbitMQ connection credentials

    Retuns:
    ----------
    rabbit_mq_creds : dict[str, any]
        rabbitMQ credentials,
        a dictionary representive of
            `broker_url` : str
            `port` : int
            `username` : str
            `password` : str
    """
    load_dotenv()

    rabbit_mq_creds = {}

    rabbit_mq_creds["broker_url"] = os.getenv("RABBIT_HOST")
    rabbit_mq_creds["port"] = os.getenv("RABBIT_PORT")
    rabbit_mq_creds["password"] = os.getenv("RABBIT_PASSWORD")
    rabbit_mq_creds["username"] = os.getenv("RABBIT_USER")

    return rabbit_mq_creds


def get_mongo_credentials():
    """
    load mongo db credentials from .env

    Returns:
    ---------
    mongo_creds : dict[str, any]
        mongodb credentials
        a dictionary representive of
            `mongo_user`: str
            `mongo_password` : str
            `mongo_host` : str
            `mongo_port` : int
    """
    load_dotenv()

    mongo_creds = {}

    mongo_creds["user"] = os.getenv("DB_USER")
    mongo_creds["password"] = os.getenv("DB_PASSWORD")
    mongo_creds["host"] = os.getenv("DB_HOST")
    mongo_creds["port"] = os.getenv("DB_PORT")

    return mongo_creds
