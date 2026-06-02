from typing import List
from model.customer import Customer, CustomerStatus
from repository import customer_repository

async def get_by_id(customer_id: int) -> Customer:
    return await customer_repository.get_by_id(customer_id)

async def get_all() -> List[Customer]:
    return await customer_repository.get_all()

async def create_customer(customer: Customer):
    if customer.status == CustomerStatus.VIP:
        vip_customers = await customer_repository.get_by_status(CustomerStatus.VIP)
        if len(vip_customers) < 10:
            return await customer_repository.create_customer(customer)
        raise Exception("Can't create any new VIP customers - out of limit")
    return await customer_repository.create_customer(customer)

async def update_customer(customer_id: int, customer: Customer):
    if customer.status == CustomerStatus.VIP:
        existing_customer = await customer_repository.get_by_id(customer_id)
        if existing_customer.status is not CustomerStatus.VIP:
            vip_customers = await customer_repository.get_by_status(CustomerStatus.VIP)
            if len(vip_customers) < 10:
                await customer_repository.update_customer(customer_id, customer)
            else:
                print(f"Can't update the customer {customer_id} to VIP - out of limit")
        else:
            await customer_repository.update_customer(customer_id, customer)
    else:
        await customer_repository.update_customer(customer_id, customer)

async def delete_by_id(customer_id: int):
    await customer_repository.delete_by_id(customer_id)
