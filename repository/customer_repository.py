from model.customer import Customer
from repository.database import database


async def get_by_id(customer_id: int):
    query = "SELECT * FROM customer WHERE id=:customer_id"
    return await database.fetch_one(query, values={"customer_id": customer_id})


async def get_all():
    query = "SELECT * FROM customer"
    return await database.fetch_all(query)


async def create_customer(customer: Customer):
    query = """
        INSERT INTO customer (first_name, last_name, email)
        VALUES (:first_name, :last_name, :email)
    """
    print("this is query: " + query)
    values = {
        "first_name": customer.first_name,
        "last_name": customer.last_name,
        "email": customer.email
    }

    await database.execute(query, values)


async def update_customer(customer_id: int, customer: Customer):
    query = """
        UPDATE customer
        SET first_name = :first_name,
            last_name = :last_name,
            email = :email
        WHERE id = :customer_id
    """
    values = {
        "customer_id": customer_id,
        "first_name": customer.first_name,
        "last_name": customer.last_name,
        "email": customer.email
    }
    await database.execute(query, values)


async def delete_by_id(customer_id: int):
    query = "DELETE FROM customer WHERE id=:customer_id"
    return await database.execute(query, values={"customer_id": customer_id})