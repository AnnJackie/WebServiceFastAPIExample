from typing import List, Optional

from starlette import status
from fastapi import APIRouter, HTTPException, Query

from model.user import User

router = APIRouter(
    prefix="/user",
    tags=["user"]
)

users = {}

@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int):
    user = users.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return user


@router.post("/", response_model=User)
async def create_user(user: User):
    if user.user_id in users:
        raise HTTPException(status_code=400, detail='User ID already exists')
    users[user.user_id] = user
    return user

@router.put("/{user_id}", response_model=User)
async def update_user(user_id: int, updated_user: User):
    if user_id not in users:
        raise HTTPException(status_code=404, detail='User not found')
    users[user_id] = updated_user
    return updated_user

@router.delete("/{user_id}", response_model=User)
async def delete_user(user_id: int):
    if user_id not in users:
        raise HTTPException(status_code=404, detail='User not found')
    return users.pop(user_id)

@router.get('/', response_model=List[User])
async def get_user_above_age(age: Optional[int] = Query(0)) -> List[User]:
    user_results = []
    for user in users.values():
        if user.age >= age:
            user_results.append(user)
    return user_results
