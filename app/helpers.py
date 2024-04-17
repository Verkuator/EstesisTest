import datetime

from . import models

def calc_avg_order_complete_time(
        total_orders: int,
        completed_orders: list[models.Order]
) -> datetime.timedelta:
    total_time = datetime.timedelta(seconds=0)
    
    for order in completed_orders:
        total_time += (order.finish_time - order.start_time)
     
    if total_orders > 0:
        avg_order_complete_time = total_time / total_orders
    else:
        avg_order_complete_time = 0
    return avg_order_complete_time


def calc_avg_day_orders(total_orders: int, days_with_orders: int) -> int:
    if days_with_orders > 0:
        avg_day_orders = total_orders // days_with_orders
    else:
        avg_day_orders = 0
    return avg_day_orders