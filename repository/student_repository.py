from model.student import Student
from repository.database import database

async def get_by_id(student_id: int):
    query = "SELECT * FROM student WHERE id=:student_id"
    return await database.fetch_one(query, values={"student_id": student_id})

async def get_all():
    query = "SELECT * FROM student"
    return await database.fetch_all(query)

async def create_student(student: Student):
    query = """
        INSERT INTO student (first_name, last_name, email)
        VALUES (:first_name, :last_name, :email)
    """
    values = {
        "first_name": student.first_name,
        "last_name": student.last_name,
        "email": student.email,
    }
    await database.execute(query, values)

async def update_student(student_id: int, student: Student):
    query = """
        UPDATE student
        SET first_name = :first_name,
            last_name = :last_name,
            email = :email
        WHERE id = :student_id
    """
    values = {
        "student_id": student_id,
        "first_name": student.first_name,
        "last_name": student.last_name,
        "email": student.email,
    }
    await database.execute(query, values)

async def delete_by_id(student_id: int):
    query = "DELETE FROM student WHERE id=:student_id"
    return await database.execute(query, values={"student_id": student_id})
