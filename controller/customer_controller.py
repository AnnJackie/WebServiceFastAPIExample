from typing import List

from fastapi import APIRouter, HTTPException

from model.customer import Customer
from repository import customer_repository

router = APIRouter(
    prefix="/customer",
    tags=["customer"]
)

@router.get("/{customer_id}", response_model=Customer)
async def get_customer(customer_id: int):
    customer = await customer_repository.get_by_id(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail=f"Customer with id: {customer_id} not found")
    return customer

@router.post("/")
async def create_customer(customer: Customer):
    print("this is customer " + str(dict(customer)))
    await customer_repository.create_customer(customer)
    return "customer creation is complete"

@router.put("/{customer_id}")
async def update_customer(customer_id: int, customer: Customer):
    existing_customer = await customer_repository.get_by_id(customer_id)
    if not existing_customer:
        raise HTTPException(status_code=404, detail=f"Can't update customer with id: {customer_id}, customer not found")
    await customer_repository.update_customer(customer_id, customer)

@router.delete("/{customer_id}", response_model=Customer)
async def delete_customer(customer_id: int):
    customer = await customer_repository.get_by_id(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail=f"Customer with id: {customer_id} not found")
    await customer_repository.delete_by_id(customer_id)
    return customer

@router.get("/", response_model=List[Customer])
async def get_customers():
    return await customer_repository.get_all()