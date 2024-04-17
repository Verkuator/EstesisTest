import datetime

from fastapi import APIRouter, Depends, exceptions, status
from sqlalchemy.orm import Session

from ..database import get_db
from app import schemas, crud, models


def calc_avg_order_complete_time(
        total_orders: int,
        completed_orders: list[models.Order]
) -> datetime.timedelta | None:
    total_time = datetime.timedelta(seconds=0)
    
    for order in completed_orders:
        total_time += (order.finish_time - order.start_time)
     
    if total_orders > 0:
        avg_order_complete_time = total_time / total_orders
    else:
        avg_order_complete_time = None
    return avg_order_complete_time


def calc_avg_day_orders(total_orders: int, days_with_orders: int) -> int | None:
    if days_with_orders > 0:
        avg_day_orders = total_orders // days_with_orders
    else:
        avg_day_orders = None
    return avg_day_orders
    

router = APIRouter(
    prefix="/courier",
    tags=["courier"])


@router.get("/", response_model=list[schemas.CourierRead])
def read_couriers(db: Session = Depends(get_db)):
    '''
        Выводит список всех курьеров
    '''
    couriers = crud.get_couriers(db)
    return couriers


@router.post("/", status_code=status.HTTP_201_CREATED)
def write_courier(courier: schemas.CourierCreate, 
                  db: Session = Depends(get_db)):
    '''
        Создаёт нового курьера в базе данных
    '''
    districts = crud.get_districts_by_name(db=db,
                                           names=courier.districts)
    if districts is None:
        raise exceptions.HTTPException(status.HTTP_400_BAD_REQUEST,
                                       detail="No such districts")
    try:
        crud.create_courier(db=db, name=courier.name, districts=districts)
    except:
        raise exceptions.HTTPException(status.HTTP_507_INSUFFICIENT_STORAGE,
                                       "can't create courier")
    
    
@router.get("/{id}", response_model=schemas.CourierInfo)
def read_courier(id: int, db: Session = Depends(get_db)):
    '''
        Выводит подробную информацию о курьере
    '''
    courier = crud.get_courier_by_id(db=db, id=id)
    if courier is None:
        raise exceptions.HTTPException(404, "courier not found")
    active_order = list(filter(lambda x: x.status == 1, courier.orders))
    if active_order:
        active_order = active_order[0]
        active_order = schemas.OrderInfo(name=active_order.name,
                                     order_id=active_order.id)
    else:
        active_order = None
    completed_orders = list(filter(lambda x: x.status == 2, courier.orders))
    
    days_with_orders = len(set(order.start_time.date() 
                               for order in completed_orders))
    total_orders = len(completed_orders)

    avg_order_complete_time = calc_avg_order_complete_time(
        total_orders=total_orders,
        completed_orders=completed_orders
    )
    
    # Рассчет среднего количества заказов в день
    avg_day_orders = calc_avg_day_orders(total_orders=total_orders,
                                         days_with_orders=days_with_orders)
    
    return schemas.CourierInfo(
        name=courier.name,
        id=courier.id,
        active_order=active_order,
        avg_day_orders=avg_day_orders,
        avg_order_complete_time=avg_order_complete_time
    )
    