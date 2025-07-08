from pydantic import BaseModel
from typing import List, Optional

class Type(BaseModel):
    id: int
    type: str
    class Config:
        from_attributes = True

class Size(BaseModel):
    id: int
    size: str
    class Config:
        from_attributes = True

class Topping(BaseModel):
    id: int
    topping: str
    class Config:
        from_attributes = True

class Flavor(BaseModel):
    id: int
    flavor: str
    class Config:
        from_attributes = True

class IceCream(BaseModel):
    id: int
    name: str
    price: float
    description: str
    images: Optional[str] = None

    type: Type
    size: Size
    topping: Optional[Topping] = None
    flavors: List[Flavor] = []

    class Config:
        from_attributes = True