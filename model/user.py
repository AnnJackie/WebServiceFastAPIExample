from datetime import date
from typing import List

from pydantic import BaseModel, Field


class User(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    age: int
    date_of_birth: date
    address: str