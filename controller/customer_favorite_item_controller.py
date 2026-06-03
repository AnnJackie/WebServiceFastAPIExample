from typing import List, Optional
from fastapi import APIRouter, HTTPException
from model.customer_favorite_item_request import CustomerFavoriteItemRequest
from model.customer_favorite_item_response import CustomerFavoriteItemResponse
from service import customer_favorite_item_service

router = APIRouter(prefix="/customer_favorite", tags=["customer_favorite"])

@router.get("/customer/{customer_id}", response_model=List[CustomerFavoriteItemResponse])
async def get_favorite_items_by_customer_id(customer_id: int) -> List[CustomerFavoriteItemResponse]:
    return await customer_favorite_item_service.get_favorite_items_by_customer_id(customer_id)

@router.get("/{favorite_item_id}", response_model=CustomerFavoriteItemResponse)
async def get_favorite_item(favorite_item_id: int) -> CustomerFavoriteItemResponse:
    favorite_item = await customer_favorite_item_service.get_by_id(favorite_item_id)
    if not favorite_item:
        raise HTTPException(status_code=404, detail=f"Favorite item with id: {favorite_item_id} not found")
    return favorite_item

@router.post("/")
async def create_favorite_item(favorite_item: CustomerFavoriteItemRequest):
    print(favorite_item)
    return await customer_favorite_item_service.create_favorite_item(favorite_item)
