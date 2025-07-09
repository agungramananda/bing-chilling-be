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

    def get_all_types(self, db: Session):
        return db.query(catalog_models.Type).all()

    def get_all_sizes(self, db: Session):
        return db.query(catalog_models.Size).all()

    def get_all_toppings(self, db: Session):
        return db.query(catalog_models.Topping).all()

    def get_all_flavors(self, db: Session):
        return db.query(catalog_models.Flavor).all()

    def add_ice_cream(self, db: Session, ice_cream_data):
        db_ice_cream = catalog_models.IceCream(
            name=ice_cream_data.name,
            price=ice_cream_data.price,
            description=ice_cream_data.description,
            images=ice_cream_data.images,
            type_id=ice_cream_data.type_id,
            size_id=ice_cream_data.size_id,
            topping_id=ice_cream_data.topping_id,
        )
        db.add(db_ice_cream)
        db.flush()  # get id

        # Add flavors (many-to-many)
        if hasattr(ice_cream_data, "flavor_ids"):
            flavors = db.query(catalog_models.Flavor).filter(
                catalog_models.Flavor.id.in_(ice_cream_data.flavor_ids)
            ).all()
            db_ice_cream.flavors = flavors

        db.commit()
        db.refresh(db_ice_cream)
        return db_ice_cream