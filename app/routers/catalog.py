from fastapi import APIRouter, Depends, HTTPException, status
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

@router.get("/types", response_model=List[catalog_schema.Type])
def get_all_types(db: Session = Depends(get_db)):
    return catalog_repo.get_all_types(db=db)

@router.get("/sizes", response_model=List[catalog_schema.Size])
def get_all_sizes(db: Session = Depends(get_db)):
    return catalog_repo.get_all_sizes(db=db)

@router.get("/toppings", response_model=List[catalog_schema.Topping])
def get_all_toppings(db: Session = Depends(get_db)):
    return catalog_repo.get_all_toppings(db=db)

@router.get("/flavors", response_model=List[catalog_schema.Flavor])
def get_all_flavors(db: Session = Depends(get_db)):
    return catalog_repo.get_all_flavors(db=db)

@router.post("/ice-creams", response_model=catalog_schema.IceCream, status_code=status.HTTP_201_CREATED)
def add_ice_cream(
    ice_cream: catalog_schema.IceCreamCreate,
    db: Session = Depends(get_db)
):
    """Endpoint untuk menambah produk es krim baru."""
    try:
        return catalog_repo.add_ice_cream(db=db, ice_cream_data=ice_cream)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))