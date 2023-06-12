import json
from pydantic import BaseModel, Field
from datetime import date as _date
from typing import Optional

class MovieUpdate(BaseModel):
    id: int
    description: Optional[str] = None
    speakers: list[dict]

class Movie(BaseModel):
    id: int
    name: str = Field(min_length=1, max_length=100)    
    date: Optional[_date] = None
    description: Optional[str] = None

    class Config:
        orm_mode = True