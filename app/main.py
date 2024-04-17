from fastapi import FastAPI

from .routers import couriers, orders


app = FastAPI(title="Delivery App",
              summary="Тествое задание для Estesis")

app.include_router(couriers.router)
app.include_router(orders.router)
