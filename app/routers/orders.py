import random
import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from app import schemas, crud


router = APIRouter(
    prefix="/order",
    tags=["order"],
)


@router.post("/{id}", status_code=status.HTTP_201_CREATED)
def finish_order(id: int, db: Session = Depends(get_db)):
    '''Завершение заказа {id}, после завершения, статус заказа меняется на 2(завершён)'''
    
    order = crud.get_order_by_id(db=db, id=id)
    if order is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "order not found")
    if order.status == 2:
        raise HTTPException(status.HTTP_409_CONFLICT, "order has finished already")
    order.finish_time = datetime.datetime.now()
    order.status = 2
    db.commit()


@router.get("/{id}", response_model=schemas.Order)
def get_order(id: int, db: Session = Depends(get_db)):
    '''
        Получение информации по заказу {id}
        
        courier_id: int
        status: int
    '''
    order = crud.get_order_by_id(db=db, id=id)
    if order is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "order not found")
    return order
        

@router.post("/", response_model=schemas.OrderCreated,
             status_code=status.HTTP_201_CREATED)
def write_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    '''
        Создание нового заказа в районе district
        доступные районы: 
            Железнодорожный
            Центральный
            Октябрьский
            Ленинский
            Индустриальный
            
        Если район не найден или нет доступных курьеров, выведет ошибку
    '''
    district = crud.get_district_by_name(db=db, name=order.district)
    if district is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "district not found")
    couriers_in_district = district.couriers

    # Проверяем, есть ли у курьеров заказы со статусом 1 (в работе)
    available_couriers = [courier for courier in couriers_in_district 
                          if not any(order.status == 1 for order in courier.orders)]
    if not available_couriers:
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "free courier not found")
    selected_courier = random.choice(available_couriers)
    order = crud.create_order(db=db, name=order.name,
                              district=district, courier_id=selected_courier.id)
    return schemas.OrderCreated(order_id=order.id, courier_id=order.courier_id)
