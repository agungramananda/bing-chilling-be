from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jose import JWTError, jwt
from .config import settings

SECRET_KEY = settings.secret_key
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_ttl

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY)
    return encoded_jwt