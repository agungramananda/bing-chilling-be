from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, Table
from sqlalchemy.orm import relationship
from core.database import Base

ice_cream_flavors_association = Table(
    'ice_cream_flavors', Base.metadata,
    Column('ice_cream_id', Integer, ForeignKey('ice_cream.id')),
    Column('flavor_id', Integer, ForeignKey('flavors.id'))
)

class Type(Base):
    __tablename__ = "types"
    id = Column(Integer, primary_key=True)
    type = Column(String(255), nullable=False)

class Size(Base):
    __tablename__ = "sizes"
    id = Column(Integer, primary_key=True)
    size = Column(String(255), nullable=False)

class Topping(Base):
    __tablename__ = "toppings"
    id = Column(Integer, primary_key=True)
    topping = Column(String(255), nullable=False)

class Flavor(Base):
    __tablename__ = "flavors"
    id = Column(Integer, primary_key=True)
    flavor = Column(String(255), nullable=False)

class IceCream(Base):
    __tablename__ = "ice_cream"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)
    description = Column(Text, nullable=False)
    images = Column(Text)

    type_id = Column(Integer, ForeignKey("types.id"))
    size_id = Column(Integer, ForeignKey("sizes.id"))
    topping_id = Column(Integer, ForeignKey("toppings.id"), nullable=True)

    type = relationship("Type")
    size = relationship("Size")
    topping = relationship("Topping")
    
    flavors = relationship(
        "Flavor",
        secondary=ice_cream_flavors_association,
        backref="ice_creams"
    )