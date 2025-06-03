import os
from dotenv import load_dotenv, find_dotenv
from sqlalchemy import create_engine
from models import Base
from sqlalchemy_utils import database_exists, create_database

load_dotenv(find_dotenv())

username = os.getenv("DATABASE_USERNAME")
password= os.getenv("DATABASE_PASSWORD")
port = os.getenv("DATABASE_PORT")
database_name = os.getenv("DATABASE_NAME")
database_url = os.getenv("DATABASE_URL")

engine = create_engine(f"postgresql://{username}:{password}@{database_url}:{port}/{database_name}", echo=True)

engine = create_engine("postgresql://localhost/mydb")
if not database_exists(engine.url):
    create_database(engine.url)

Base.metadata.create_all(engine)
