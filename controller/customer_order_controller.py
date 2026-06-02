from fastapi import APIRouter, HTTPException
from model.customer_order import CustomerOrder
from model.customer_order_request import CustomerOrderRequest
from model.customer_order_response import CustomerOrderResponse
from service import customer_order_service

router = APIRouter(prefix="/customer_order", tags=["customer_order"])

@router.get("/{customer_order_id}", response_model=CustomerOrder)
async def get_customer_order(customer_order_id: int):
    customer_order = await customer_order_service.get_by_id(customer_order_id)
    if not customer_order:
        raise HTTPException(status_code=404, detail=f"Customer order with id: {customer_order_id} not found")
    return customer_order

@router.post("/", response_model=CustomerOrderResponse)
async def create_customer_order(customer_order_request: CustomerOrderRequest):
    return await customer_order_service.create_customer_order(customer_order_request)

@router.put("/{customer_order_id}", response_model=CustomerOrderResponse)
async def update_customer_order(customer_order_id: int, customer_order_request: CustomerOrderRequest):
    try:
        return await customer_order_service.update_customer_order(customer_order_id, customer_order_request)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{customer_order_id}")
async def delete_customer_order(customer_order_id: int):
    customer_order = await customer_order_service.get_by_id(customer_order_id)
    if not customer_order:
        raise HTTPException(status_code=404, detail=f"Customer order with id: {customer_order_id} not found")
    await customer_order_service.delete_by_id(customer_order_id)
