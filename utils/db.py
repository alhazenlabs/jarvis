import os
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from data_api.models import Base
from utils.constants import Constants
from utils.logger import LOG


SQLITE_PREFIX = "sqlite:///"
DATABASE = Constants.MEDIA_FOLDER + Constants.SQLITE_DB
ECHO = True if Constants.LOG_LEVEL == "DEBUG" else False


def get_engine():
    """
    Create and return a SQLAlchemy engine for the SQLite database.

    Returns:
        sqlalchemy.engine.base.Engine: SQLAlchemy engine for the SQLite database.
    """
    return create_engine(SQLITE_PREFIX + DATABASE, echo=ECHO)


def load_db():
    """
    Load the database or create it if it doesn't exist.

    This function checks if the SQLite database file exists and creates it if it's not found.

    Returns:
        None
    """
    if not os.path.exists(DATABASE):
        LOG.info("Database doesn't exists creating it...")
        engine = get_engine()
        Base.metadata.create_all(engine)
    else:
        LOG.info("Found a database, hence skipping the creation")


def session():
    """
    Create and return a SQLAlchemy session bound to the database engine.

    Returns:
        sqlalchemy.orm.session.Session: SQLAlchemy session.
    """
    # Return sqlalchemy session to database
    return Session(bind=get_engine(), expire_on_commit=False)


@contextmanager
def terminating_sn():
    """
    A context manager that provides a SQLAlchemy session and closes it after use.

    Usage:
        with terminating_sn() as sn:
            # Use the SQLAlchemy session 'sn' here.

    Returns:
        sqlalchemy.orm.session.Session: SQLAlchemy session.
    """
    # A context manager which closes session and db connections after use
    sn = session()
    try:
        yield sn
    finally:
        sn.close()
        sn.bind.dispose()
