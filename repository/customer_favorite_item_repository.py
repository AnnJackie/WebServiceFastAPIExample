from typing import List, Optional
from model.customer_favorite_item import CustomerFavoriteItem
from repository.database import database

TABLE_NAME = "customer_favorite_item"

async def get_by_id(favorite_item_id: int) -> Optional[CustomerFavoriteItem]:
    query = f"SELECT * FROM {TABLE_NAME} WHERE id=:favorite_item_id"
    row = await database.fetch_one(query, values={"favorite_item_id": favorite_item_id})
    if row is None:
        return None
    return CustomerFavoriteItem.model_validate(dict(row))

async def get_favorite_items_by_customer_id(customer_id: int) -> List[CustomerFavoriteItem]:
    query = f"SELECT * FROM {TABLE_NAME} WHERE customer_id=:customer_id"
    rows = await database.fetch_all(query, values={"customer_id": customer_id})
    return [CustomerFavoriteItem.model_validate(dict(row)) for row in rows]

async def get_by_customer_id_and_item_id(customer_id: int, item_id: int) -> Optional[CustomerFavoriteItem]:
    query = f"SELECT * FROM {TABLE_NAME} WHERE customer_id=:customer_id AND item_id=:item_id"
    row = await database.fetch_one(query, values={"customer_id": customer_id, "item_id": item_id})
    if row is None:
        return None
    return CustomerFavoriteItem.model_validate(dict(row))

async def create_favorite_item(favorite_item: CustomerFavoriteItem) -> int:
    query = f"""
        INSERT INTO {TABLE_NAME} (customer_id, item_id)
        VALUES (:customer_id, :item_id)
    """
    values = {
        "customer_id": favorite_item.customer_id,
        "item_id": favorite_item.item_id,
    }
    async with database.transaction():
        await database.execute(query, values)
        last_record_id = await database.fetch_one("SELECT LAST_INSERT_ID()")
    return last_record_id[0]

async def update_favorite_item(favorite_item_id: int, favorite_item: CustomerFavoriteItem):
    query = f"""
        UPDATE {TABLE_NAME}
        SET customer_id = :customer_id,
            item_id = :item_id
        WHERE id = :favorite_item_id
    """
    values = {
        "favorite_item_id": favorite_item_id,
        "customer_id": favorite_item.customer_id,
        "item_id": favorite_item.item_id,
    }
    await database.execute(query, values)

async def delete_by_id(favorite_item_id: int):
    query = f"DELETE FROM {TABLE_NAME} WHERE id=:favorite_item_id"
    return await database.execute(query, values={"favorite_item_id": favorite_item_id})
