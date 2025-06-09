from contextlib import contextmanager
import os
from typing import Generator
from dotenv import load_dotenv, find_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from database.models import Base
from sqlalchemy_utils import database_exists, create_database

load_dotenv(find_dotenv())

username = os.getenv("DATABASE_USERNAME")
password = os.getenv("DATABASE_PASSWORD")
port = os.getenv("DATABASE_PORT")
database_name = os.getenv("DATABASE_NAME")
database_host = os.getenv("DATABASE_HOST")

DATABASE_URL = (
    f"postgresql://{username}:{password}@{database_host}:{port}/{database_name}"
)

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_db():
    if not database_exists(engine.url):
        create_database(engine.url)


def create_schema():
    Base.metadata.create_all(engine)


# FastAPI dependency
def get_db_session() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


@contextmanager
def get_db_context() -> Generator[Session, None, None]:
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
