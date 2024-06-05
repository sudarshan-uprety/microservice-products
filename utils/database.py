from mongoengine import connect

from utils import variables

def get_db_connection_url() -> str:
    url = variables.DB
    if url is None:
        raise ValueError("DB URL not defined")
    return url


def db_config() -> None:
    try:
        uri: str = get_db_connection_url()
        connect(host=uri)
    except Exception as err:
        connect("mongoenginetest", host="mongomock://localhost")
        raise ValueError(str(err))