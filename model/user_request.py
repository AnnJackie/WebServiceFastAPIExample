from pydantic import BaseModel

class UserRequest(BaseModel):
    username: str
    first_name: str
    last_name: str
    password: str
