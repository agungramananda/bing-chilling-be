from pydantic import BaseModel
from typing import List
from datetime import datetime
from .catalog_schema import IceCream as IceCreamSchema

class OrderItemBase(BaseModel):
    ice_cream_id: int
    quantity: int

class OrderItemCreate(OrderItemBase):
    pass

class OrderItem(OrderItemBase):
    id: int
    price_at_purchase: float
    ice_cream: IceCreamSchema 

    class Config:
        from_attributes = True

class Order(BaseModel):
    id: int
    total_amount: float
    status: str
    created_at: datetime
    items: List[OrderItem]

    class Config:
        from_attributes = True