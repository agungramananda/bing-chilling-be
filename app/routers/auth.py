from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from core.database import get_db
from core.security import create_access_token, verify_password
from repositories.user_repository import UserRepository
from schemas import user_schema, token_schema

router = APIRouter(prefix="/auth", tags=["Authentication"])
user_repo = UserRepository()

@router.post("/register", response_model=user_schema.User)
def register(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    db_user = user_repo.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_repo.create_user(db=db, user=user)

@router.post("/login", response_model=token_schema.Token)
def login(user_credentials: user_schema.UserLogin, db: Session = Depends(get_db)):
    user = user_repo.get_user_by_email(db, email=user_credentials.email)
    if not user or not verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}