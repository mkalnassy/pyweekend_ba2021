from os import getenv
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.engine import Connection

DATABASE_DSN = getenv("DATABASE_DSN")

engine = create_engine(DATABASE_DSN)

def db_connection() -> Generator[Connection, None, None]:
    """Connect to the DB, initialize an isolated transaction and yield that connection.
    
    This already comes with a predefined pooling method which is a way how to keep several connections to the DB open
    in memory and effcently reuse them in multiple queries.
    Default pool is a `QueuePool` (https://docs.sqlalchemy.org/en/14/core/pooling.html#sqlalchemy.pool.QueuePool) with
    `5` maintained connections.
    """
    with engine.connect() as connection:
        with connection.begin():
            yield connection
