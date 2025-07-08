from sqlalchemy.orm import Session, joinedload
from models import catalog as catalog_models

class CatalogRepository:
    def get_all_ice_creams(self, db: Session):
        """Mengambil semua produk es krim dengan data relasinya."""
        return db.query(catalog_models.IceCream).options(
            joinedload(catalog_models.IceCream.type),
            joinedload(catalog_models.IceCream.size),
            joinedload(catalog_models.IceCream.topping),
            joinedload(catalog_models.IceCream.flavors)
        ).all()