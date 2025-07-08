from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from .database import get_db
from schemas import token_schema, user_schema
from repositories.user_repository import UserRepository
from .security import SECRET_KEY
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

user_repo = UserRepository()

def get_current_user(
    token: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_db)
) -> user_schema.User:
    """
    Mendekode token JWT untuk mendapatkan email pengguna, 
    lalu mengambil data pengguna dari database.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY)
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = token_schema.TokenData(email=email)
    except JWTError:
        raise credentials_exception
    
    user = user_repo.get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
        
    return user