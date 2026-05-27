from fastapi import FastAPI
from controller.user_controller import router as user_router
from controller.order_controller import router as order_router

app = FastAPI()
app.include_router(user_router)
app.include_router(order_router)

