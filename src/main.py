import os
from dotenv import load_dotenv, find_dotenv
from sqlalchemy import text, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

load_dotenv(find_dotenv())

username = os.getenv("DATABASE_USERNAME")
password= os.getenv("DATABASE_PASSWORD")
port = os.getenv("DATABASE_PORT")
database_name = os.getenv("DATABASE_NAME")
database_url = os.getenv("DATABASE_URL")

engine = create_engine(f"postgresql://{username}:{password}@{database_url}:{port}/", echo=True)

class Base(DeclarativeBase):
    pass

try:
    with engine.connect() as connection:
        print("Connection successful!")
except Exception as e:
    print(f"Connection failed: {e}")