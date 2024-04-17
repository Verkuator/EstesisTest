import datetime

from sqlalchemy import (
    Column, 
    Integer, 
    String, 
    SmallInteger, 
    DateTime, 
    Table,
    ForeignKey
)
from sqlalchemy.orm import relationship, Mapped, mapped_column

# from database import Base, engine
from .database import Base, engine


DistrictCourier = Table(
    "district_courier",
    Base.metadata,
    Column("district_id", ForeignKey("districts.id"), primary_key=True),
    Column("courier_id", ForeignKey("couriers.id"), primary_key=True)
)


class District(Base):
    __tablename__ = "districts"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))

    couriers: Mapped[list["Courier"]] = relationship(
        secondary=DistrictCourier, back_populates="districts"
    )
    orders: Mapped[list["Order"]] = relationship()


class Courier(Base):
    __tablename__ = "couriers"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name = mapped_column(String)
    
    districts: Mapped[list["District"]] = relationship(
        secondary=DistrictCourier, back_populates="couriers"
    )
    orders: Mapped[list["Order"]] = relationship()


class Order(Base):
    __tablename__ = "orders"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    status: Mapped[int] = mapped_column(SmallInteger) 
    start_time: Mapped[datetime.datetime] = mapped_column(DateTime)
    finish_time: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True)
    courier_id: Mapped[int] = mapped_column(ForeignKey("couriers.id"))
    district_id: Mapped[int] = mapped_column(ForeignKey("districts.id"))
    
    couier: Mapped[Courier] = relationship(back_populates="orders")
    district: Mapped[District] = relationship(back_populates="orders")


if __name__ == "__main__":
    Base.metadata.create_all(engine)
