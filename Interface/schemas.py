import json
from pydantic import BaseModel, Field
from datetime import date as _date
from typing import Optional

class MovieUpdate(BaseModel):
    id: int
    description: Optional[str] = ""
    speakers: list[dict]

class Movie(BaseModel):
    id: int
    name: str = Field(min_length=1, max_length=100)    
    date: Optional[_date] = ""
    description: Optional[str] = ""

    class Config:
        orm_mode = True

class Message(BaseModel):
    name: str
    email: str
    message: str

    def dict_format(self):
        return {
            'name': self.name.strip(),
            'email': self.email.strip(),
            'message': self.message.strip()
        }

    def is_ok(self):
        if (self.name != "") and (self.email != "") and (self.message != ""):
            return True
        return False