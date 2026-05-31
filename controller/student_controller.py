from typing import List

from fastapi import APIRouter, HTTPException

from model.student import Student
from repository import student_repository

router = APIRouter(
    prefix="/student",
    tags=["student"],
)


@router.get("/{student_id}", response_model=Student)
async def get_student(student_id: int):
    student = await student_repository.get_by_id(student_id)
    if not student:
        raise HTTPException(status_code=404, detail=f"Student with id: {student_id} not found")
    return student


@router.post("/")
async def create_student(student: Student):
    await student_repository.create_student(student)
    return "student creation is complete"


@router.put("/{student_id}")
async def update_student(student_id: int, student: Student):
    existing_student = await student_repository.get_by_id(student_id)
    if not existing_student:
        raise HTTPException(
            status_code=404,
            detail=f"Can't update student with id: {student_id}, student not found",
        )
    await student_repository.update_student(student_id, student)


@router.delete("/{student_id}", response_model=Student)
async def delete_student(student_id: int):
    student = await student_repository.get_by_id(student_id)
    if not student:
        raise HTTPException(status_code=404, detail=f"Student with id: {student_id} not found")
    await student_repository.delete_by_id(student_id)
    return student


@router.get("/", response_model=List[Student])
async def get_students():
    return await student_repository.get_all()
