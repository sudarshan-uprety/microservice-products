import os
from dotenv import load_dotenv
from mongoengine import connect

load_dotenv()


def get_db_connection_url() -> str:
    url = os.getenv("DB")
    if url is None:
        raise ValueError("DB URL not defined")
    return url


def db_config() -> None:
    try:
        uri: str = get_db_connection_url()
        connect(host=uri)
    except Exception as err:
        raise ValueError(str(err))