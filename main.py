from fastapi import FastAPI
from controller.user_controller import router as user_router
from controller.order_controller import router as order_router
from controller.customer_controller import router as customer_router
from controller.student_controller import router as student_router
from controller.customer_order_controller import router as customer_order_router
from repository.database import database

app = FastAPI()
app.include_router(user_router)
app.include_router(order_router)
app.include_router(customer_router)
app.include_router(customer_order_router)
app.include_router(student_router)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
