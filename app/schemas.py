import datetime
from typing import Optional
from pydantic import BaseModel


class District(BaseModel):
    name: str


class CourierBase(BaseModel):
    name: str


class CourierRead(CourierBase):
    id: int


class CourierCreate(CourierBase):
    districts: list[str] = []


class CourierInfo(CourierRead):
    active_order: Optional["OrderInfo"]
    avg_order_complete_time: datetime.timedelta
    avg_day_orders: int
    
    
class OrderBase(BaseModel):
    name: str


class OrderInfo(OrderBase):
    order_id: int


class OrderCreate(OrderBase):
    district: str


class OrderCreated(BaseModel):
    order_id: int
    courier_id: int


class Order(BaseModel):
    courier_id: int
    status: int


