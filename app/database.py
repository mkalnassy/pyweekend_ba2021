from os import getenv
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.engine import Connection

DATABASE_DSN = getenv("DATABASE_DSN")

engine = create_engine(DATABASE_DSN)

def db_connection() -> Generator[Connection, None, None]:
    with engine.connect() as connection:
        with connection.begin():
            yield connection
