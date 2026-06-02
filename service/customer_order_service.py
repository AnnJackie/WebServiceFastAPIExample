from model.customer import Customer
from model.customer_order import CustomerOrder
from model.customer_order_request import CustomerOrderRequest
from model.customer_order_response import CustomerOrderResponse
from repository import customer_order_repository
from service import customer_service

async def get_by_id(customer_order_id: int) -> CustomerOrder:
    return await customer_order_repository.get_by_id(customer_order_id)

async def create_customer_order(customer_order_request: CustomerOrderRequest) -> CustomerOrderResponse:
    selected_customer = customer_order_request.customer
    if selected_customer.id is None:
        created_customer_id = await customer_service.create_customer(selected_customer)
        selected_customer = await customer_service.get_by_id(created_customer_id)
        customer_order_request.customer_order.customer_id = created_customer_id
    else:
        existing_customer = await customer_service.get_by_id(selected_customer.id)
        if not existing_customer:
            raise Exception(f"Can't find existing customer with id: {selected_customer.id}")
    customer_order_request.customer_order.customer_id = selected_customer.id
    customer_order_request.customer = selected_customer
    customer_order = customer_order_request.customer_order
    await customer_order_repository.create_customer_order(customer_order)
    customer_orders = await customer_order_repository.get_by_customer_id(selected_customer.id)
    return CustomerOrderResponse(customer=selected_customer, customer_orders=customer_orders)

async def update_customer_order(customer_order_id: int, customer_order_request: CustomerOrderRequest) -> CustomerOrderResponse:
    existing_order = await customer_order_repository.get_by_id(customer_order_id)
    if not existing_order:
        raise Exception(f"Can't find existing customer order with id: {customer_order_id}")
    customer = customer_order_request.customer
    customer_order = customer_order_request.customer_order
    customer_order.customer_id = customer.id
    await customer_service.update_customer(customer.id, customer)
    await customer_order_repository.update_customer_order(customer_order_id, customer_order)
    customer_orders = await customer_order_repository.get_by_customer_id(customer.id)
    return CustomerOrderResponse(customer=customer, customer_orders=customer_orders)

async def delete_by_id(customer_order_id: int):
    await customer_order_repository.delete_by_id(customer_order_id)
