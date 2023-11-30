import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

user = os.environ.get('DATABASE_OWNER')
password = os.environ.get('DATABASE_PASSWORD')

SQLALCHEMY_DATABASE_URL = f"postgresql://{user}:{password}@localhost/userItemAPI-database"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
