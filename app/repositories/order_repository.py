from sqlalchemy.orm import Session, joinedload
from models import order as order_model, catalog as catalog_model
from schemas import order_schema

class OrderRepository:
    def get_orders_by_user(self, db: Session, user_id: int):
        return db.query(order_model.Order).filter(order_model.Order.user_id == user_id).options(
            joinedload(order_model.Order.items).joinedload(order_model.OrderItem.ice_cream)
        ).all()

    def create_order(self, db: Session, user_id: int, order: order_schema.OrderCreate):
        db_order = order_model.Order(user_id=user_id, total_amount=0)
        db.add(db_order)
        db.flush()

        total = 0
        for item in order.items:
            ice_cream = db.query(catalog_model.IceCream).filter(catalog_model.IceCream.id == item.ice_cream_id).first()
            if not ice_cream:
                raise Exception("Ice cream not found")

            item_price = float(ice_cream.price)
            total += item_price * item.quantity
            
            db_item = order_model.OrderItem(
                order_id=db_order.id,
                ice_cream_id=item.ice_cream_id,
                quantity=item.quantity,
                price_at_purchase=item_price
            )
            db.add(db_item)

        db_order.total_amount = total
        db.commit()
        db.refresh(db_order)
        return db_order