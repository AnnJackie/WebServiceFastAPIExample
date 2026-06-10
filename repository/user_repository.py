from typing import Optional
from model.user import User
from model.user_request import UserRequest
from repository.database import database

async def get_by_username(username: str) -> Optional[User]:
    query = "SELECT * FROM users WHERE username=:username"
    row = await database.fetch_one(query, values={"username": username})
    if row:
        print(row)
        return User.model_validate(dict(row))
    return None

async def get_by_id(user_id: int) -> Optional[User]:
    query = "SELECT * FROM users WHERE id=:user_id"
    row = await database.fetch_one(query, values={"user_id": user_id})
    if row:
        return User.model_validate(dict(row))
    return None

async def create_user(user: UserRequest, hashed_password: str):
    query = """
        INSERT INTO users (username, first_name, last_name, hashed_password)
        VALUES (:username, :first_name, :last_name, :hashed_password)
    """
    user_dict = user.model_dump()
    user_dict.pop("password")
    values = {**user_dict, "hashed_password": hashed_password}
    await database.execute(query, values)
