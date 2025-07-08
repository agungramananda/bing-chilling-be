from sqlalchemy.orm import Session
from models import users as user_model
from schemas import user_schema
from core.security import get_password_hash

class UserRepository:
    def get_user_by_email(self, db: Session, email: str):
        return db.query(user_model.User).filter(user_model.User.email == email).first()

    def create_user(self, db: Session, user: user_schema.UserCreate):
        hashed_password = get_password_hash(user.password)
        db_user = user_model.User(email=user.email, name=user.name, hashed_password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user