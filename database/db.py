from contextlib import contextmanager
import os
from typing import Generator
from dotenv import load_dotenv, find_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Base
from sqlalchemy_utils import database_exists, create_database

load_dotenv(find_dotenv())

username = os.getenv("DATABASE_USERNAME")
password= os.getenv("DATABASE_PASSWORD")
port = os.getenv("DATABASE_PORT")
database_name = os.getenv("DATABASE_NAME")
database_host = os.getenv("DATABASE_URL")

DATABASE_URL = f"postgresql://{username}:{password}@{database_host}:{port}/{database_name}"

engine = create_engine(DATABASE_URL, echo=True)
session_maker = sessionmaker(bind=engine)

def create_db():
    if not database_exists(engine.url):
        create_database(engine.url)

def create_schema():
    Base.metadata.create_all(engine)

@contextmanager
def get_db_session() -> Generator:
    session = session_maker()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

create_db()
create_schema()