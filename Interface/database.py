import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .main import ROOT_PATH

SQLALCHEMY_DATABASE_URL = "sqlite:///" + os.path.join(ROOT_PATH, "samsa.db")

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# db connection
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()