import os
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from utils.constants import Constants
from utils.models import Base
from utils.logger import LOG

SQLITE_PREFIX = "sqlite:///"
DATABASE = Constants.MEDIA_FOLDER + "jarvis.db"
ECHO = True if LOG.level == "DEBUG" else False

def get_engine():
    return create_engine(SQLITE_PREFIX + DATABASE, echo=ECHO)


def load_db():
    if not os.path.exists(DATABASE):
        LOG.info("Database doesn't exists creating it...")
        engine = get_engine()
        Base.metadata.create_all(engine)
    else:
        LOG.info("Found a database, hence skipping the creation")


def session():
    # Return sqlalchemy session to database
    return Session(bind=get_engine(), expire_on_commit=False)


@contextmanager
def terminating_sn():
    # A context manager which closes session and db connections after use
    sn = session()
    try:
        yield sn
    finally:
        sn.close()
        sn.bind.dispose()
