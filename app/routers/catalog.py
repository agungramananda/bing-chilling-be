from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from repositories.catalog_repository import CatalogRepository
from schemas import catalog_schema

router = APIRouter(
    prefix="/catalog",
    tags=["Catalog"],
)

catalog_repo = CatalogRepository()

@router.get("/ice-creams", response_model=List[catalog_schema.IceCream])
def get_all_ice_creams(db: Session = Depends(get_db)):
    """Endpoint untuk mendapatkan daftar semua produk es krim."""
    return catalog_repo.get_all_ice_creams(db=db)