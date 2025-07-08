from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from core.dependencies import get_current_user 
from repositories.order_repository import OrderRepository
from schemas import order_schema, user_schema

router = APIRouter(prefix="/orders", tags=["Orders"])
order_repo = OrderRepository()

@router.post("/", response_model=order_schema.Order, status_code=status.HTTP_201_CREATED)
def create_new_order(
    order: order_schema.OrderItemCreate,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(get_current_user)
):
    """Membuat pesanan baru untuk pengguna yang sedang login."""
    try:
        return order_repo.create_order(db=db, user_id=current_user.id, order=order)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/me", response_model=List[order_schema.Order])
def get_my_orders(
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(get_current_user)
):
    """Melihat riwayat pesanan dari pengguna yang sedang login."""
    return order_repo.get_orders_by_user(db=db, user_id=current_user.id)