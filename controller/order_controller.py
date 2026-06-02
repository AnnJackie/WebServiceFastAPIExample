from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, Header
from model.order import Order

router = APIRouter(prefix="/order", tags=["order"])
orders = {}

@router.get("/{order_id}", response_model=Order)
async def get_order(order_id: int, authorization: Optional[str] = Header(None)):
    print(authorization)
    if authorization:
        order = orders.get(order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return order
    raise HTTPException(status_code=401, detail="Unauthorized user!")

@router.post("/", response_model=Order)
async def create_order(order: Order):
    if order.order_id in orders:
        raise HTTPException(status_code=400, detail="Order ID already exists")
    orders[order.order_id] = order
    return order

@router.put("/{order_id}", response_model=Order)
async def update_order(order_id: int, updated_order: Order):
    if order_id not in orders:
        raise HTTPException(status_code=404, detail="Order not found")
    orders[order_id] = updated_order
    return updated_order

@router.delete("/{order_id}", response_model=Order)
async def delete_order(order_id: int):
    if order_id not in orders:
        raise HTTPException(status_code=404, detail="Order not found")
    return orders.pop(order_id)

@router.get("/", response_model=List[Order])
async def get_order_by_customer(customer_name: Optional[str] = Query(None)) -> List[Order]:
    return [order for order in orders.values() if order.customer_name == customer_name]
