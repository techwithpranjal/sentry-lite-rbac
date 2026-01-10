from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from passlib.hash import bcrypt

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.core.settings import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def hash_password(password: str) -> str:
    password = password.encode("utf-8")[:settings.MAX_BCRYPT_BYTES].decode("utf-8", "ignore")
    return bcrypt.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
                to_encode, 
                settings.JWT_SECRET_KEY, 
                algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

def get_logged_user(token: str = Depends(oauth2_scheme)) -> Optional[dict]:
    """Extract user information from JWT token in request headers."""

    try:
        user_data = jwt.decode(token, 
                             settings.JWT_SECRET_KEY, 
                             algorithms=[settings.JWT_ALGORITHM])

        if user_data is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token.")
        
        return {"sub": user_data}
        
    except JWTError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token.")   

def require_admin(current_user: dict = Depends(get_logged_user)):
    if not current_user["sub"].get("is_super_admin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user