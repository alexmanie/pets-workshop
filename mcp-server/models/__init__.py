import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .base import Base
from .breed import Breed
from .dog import Dog

# Path to the shared SQLite database in the server/ directory
_server_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'server')
_db_path = os.path.join(_server_dir, 'dogshelter.db')
_engine = create_engine(f'sqlite:///{_db_path}')

Session = sessionmaker(bind=_engine)


def get_session():
    return Session()
