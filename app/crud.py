import datetime

from sqlalchemy.orm import Session

from app import models


def get_courier_by_id(db: Session, id: int):
    return db.query(models.Courier).filter_by(id=id).first()


def get_couriers(db: Session):
    return db.query(models.Courier).all()


def create_courier(db: Session, name: str, districts: list[models.District]):

    db_courier = models.Courier(name=name,
                                districts=districts)
    db.add(db_courier)
    db.commit()
    db.refresh(db_courier)
    return db_courier


def get_districts_by_name(db: Session, names: list[str]):
    db_districts = db.query(models.District).where(
        models.District.name.in_(names)
    ).all()
    return db_districts


def get_district_by_name(db: Session, name: str):
    return db.query(models.District).filter_by(name=name).first()


def create_order(
    db: Session, 
    name: str, 
    courier_id: int, 
    district: models.District
):
    order = models.Order(name=name,
                         courier_id=courier_id,
                         status=1,
                         start_time=datetime.datetime.now(),
                         district_id=district.id)
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


def get_order_by_id(db: Session, id: int):
    return db.query(models.Order).filter_by(id=id).first()
