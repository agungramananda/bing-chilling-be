from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from core.database import Base

from sqlalchemy.orm import relationship

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    total_amount = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey("users.id"))
    items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Integer)
    price_at_purchase = Column(Float)
    order_id = Column(Integer, ForeignKey("orders.id"))
    order = relationship("Order", back_populates="items")
    ice_cream_id = Column(Integer, ForeignKey("ice_cream.id"))
    ice_cream = relationship("IceCream")