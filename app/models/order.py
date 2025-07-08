from sqlalchemy import Column, Integer, Float, DateTime, String, ForeignKey
from sqlalchemy.sql import func
from core.database import Base

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    total_amount = Column(Float)
    status = Column(String, default="pending") # misal: pending, paid, completed
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey("users.id"))

class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Integer)
    price_at_purchase = Column(Float)
    order_id = Column(Integer, ForeignKey("orders.id"))
    flavor_id = Column(Integer, ForeignKey("flavors.id"))