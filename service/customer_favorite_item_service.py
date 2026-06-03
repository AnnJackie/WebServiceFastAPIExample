from typing import List, Optional

from fastapi import HTTPException
from model.customer_favorite_item import CustomerFavoriteItem
from model.customer_favorite_item_request import CustomerFavoriteItemRequest
from model.customer_favorite_item_response import CustomerFavoriteItemResponse
from repository import customer_favorite_item_repository
from service import customer_service
from api.internal_api import seller_service_api

async def get_by_id(favorite_item_id: int) -> Optional[CustomerFavoriteItemResponse]:
    customer_favorite_item = await customer_favorite_item_repository.get_by_id(favorite_item_id)
    if customer_favorite_item:
        item = await seller_service_api.get_item_by_item_id(customer_favorite_item.item_id)
        if item:
            return CustomerFavoriteItemResponse(
                id=customer_favorite_item.id,
                customer_id=customer_favorite_item.customer_id,
                item_response=item,
            )
    return None

async def get_favorite_items_by_customer_id(customer_id: int) -> List[CustomerFavoriteItemResponse]:
    customer_favorite_items = await customer_favorite_item_repository.get_favorite_items_by_customer_id(customer_id)
    response_list = []
    for favorite_item in customer_favorite_items:
        item = await seller_service_api.get_item_by_item_id(favorite_item.item_id)
        if item:
            response_list.append(
                CustomerFavoriteItemResponse(
                    id=favorite_item.id,
                    customer_id=favorite_item.customer_id,
                    item_response=item,
                )
            )
    return response_list

async def create_favorite_item(customer_favorite_item_request: CustomerFavoriteItemRequest) -> Optional[int]:
    customer = await customer_service.get_by_id(customer_favorite_item_request.customer_id)
    if customer:
        item_details = await seller_service_api.get_lowest_price_item_by_name(customer_favorite_item_request.item_name)
        print(item_details)
        print(customer.id)
        print(item_details.id)
        if item_details is not None:
            existing_favorite_item = await customer_favorite_item_repository.get_by_customer_id_and_item_id(
                customer.id, item_details.id
            )
            if not existing_favorite_item:
                return await customer_favorite_item_repository.create_favorite_item(
                    CustomerFavoriteItem(customer_id=customer.id, item_id=item_details.id)
                )
    raise HTTPException(status_code=404, detail=f"Customer not found")