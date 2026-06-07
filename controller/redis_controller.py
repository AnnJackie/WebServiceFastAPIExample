from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from model.user import User
from repository.redis_manager import redis_client

router = APIRouter(prefix="/redis", tags=["redis"])

@router.post("/test")
async def redis_test(redis_key: str, redis_value: str):
    try:
        redis_client.set(redis_key, redis_value)
        return {"message": "Redis test is complete"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
