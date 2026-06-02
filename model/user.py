from datetime import date
from pydantic import BaseModel

class User(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    age: int
    date_of_birth: date
    address: str
