from model.customer import Customer, CustomerStatus
from repository import cache_repository
from repository.database import database

async def get_by_id(customer_id: int):
    if cache_repository.does_key_exist(f"{customer_id}"):
        string_customer = cache_repository.get_cache_entity(f"{customer_id}")
        customer = Customer.model_validate_json(string_customer)
        return customer
    else:
        query = "SELECT * FROM customer WHERE id=:customer_id"
        row = await database.fetch_one(query, values={"customer_id": customer_id})
        if row is None:
            return None
        customer = Customer.model_validate(dict(row))
        cache_repository.create_cache_entity(f"{customer_id}", customer.model_dump_json())
        return customer


async def get_all():
    query = "SELECT * FROM customer"
    rows = await database.fetch_all(query)
    return [Customer.model_validate(dict(row)) for row in rows]

async def create_customer(customer: Customer):
    query = """
        INSERT INTO customer (first_name, last_name, email, status)
        VALUES (:first_name, :last_name, :email, :status)
    """
    values = {
        "first_name": customer.first_name,
        "last_name": customer.last_name,
        "email": customer.email,
        "status": customer.status.name,
    }
    async with database.transaction():
        await database.execute(query, values)
        last_record_id = await database.fetch_one("SELECT LAST_INSERT_ID()")
    
    customer_id = last_record_id[0]
    customer.id = customer_id
    cache_repository.create_cache_entity(f"{customer_id}", customer.model_dump_json())
    return customer_id

async def update_customer(customer_id: int, customer: Customer):
    cache_repository.update_cache_entity(f"{customer_id}", customer.model_dump_json())

    query = """
        UPDATE customer
        SET first_name = :first_name,
            last_name = :last_name,
            email = :email,
            status = :status
        WHERE id = :customer_id
    """
    values = {
        "customer_id": customer_id,
        "first_name": customer.first_name,
        "last_name": customer.last_name,
        "email": customer.email,
        "status": customer.status.name,
    }
    await database.execute(query, values)

async def delete_by_id(customer_id: int):
    cache_repository.remove_cache_entity(f"{customer_id}")
    
    query = "DELETE FROM customer WHERE id=:customer_id"
    return await database.execute(query, values={"customer_id": customer_id})

async def get_by_status(customer_status: CustomerStatus):
    query = "SELECT * FROM customer WHERE status=:customer_status"
    rows = await database.fetch_all(query, values={"customer_status": customer_status.name})
    return [Customer.model_validate(dict(row)) for row in rows]
