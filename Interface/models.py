import json 

from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import Session

from .database import Base, SessionLocal

class MovieDB(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    date = Column(Date, nullable=True)
    description = Column(String, nullable=True)
    
    def __repr__(self):
       return "<Movie(id='%s', name='%s')>" % (self.id, self.name)