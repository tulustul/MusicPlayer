import os
from pathlib import Path

from typing import cast

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

from core.config import config

Base = declarative_base()
session = None


def init():
    global session

    db_path = Path(config['db_file']).expanduser()
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    engine = create_engine(
        f'sqlite:///{db_path}',
        connect_args={'check_same_thread': False},
    )
    Base.metadata.create_all(engine)
    DBSession = sessionmaker(bind=engine)
    session = DBSession()


def get_session() -> Session:
    return cast(Session, session)
