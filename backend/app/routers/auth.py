from app.models import User
from app.core.security import hash_password, verify_password, create_access_token
from app.schemas import UserRegister, UserRead, LoginRequest, TokenResponse
from app.db import get_session
from app.queries import GET_USER_BY_EMAIL, INSERT_USER
from app.core.settings import settings

from datetime import timedelta, datetime

from sqlmodel import Session
from fastapi import APIRouter, Depends, HTTPException, status



router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register_user(user: UserRegister, session: Session = Depends(get_session)):
    """Register a new user using email and password."""

    result = session.exec(GET_USER_BY_EMAIL.params({"email": user.email}))
    existing_user = result.first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    password_hash = hash_password(user.password)
    result = session.exec(
        INSERT_USER.params(
            {
                "email": user.email, 
                "password_hash": password_hash,
                "created_at": datetime.utcnow()
            })
    )
    session.commit()

    result = session.exec(GET_USER_BY_EMAIL.params({"email": user.email}))
    row = result.first()
    new_user = User(
        id=row.id,
        email=row.email,
        created_at=row.created_at
    )
    return new_user


@router.post("/login", response_model=TokenResponse)
def login_user(login_req: LoginRequest, session: Session = Depends(get_session)):
    """Authenticate user and return access token."""
    
    result = session.exec(GET_USER_BY_EMAIL.params({"email": login_req.email}))
    user = result.first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email or password.")

    if not verify_password(login_req.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email or password.")
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": {"user_id": user.id, "email": user.email}},
        expires_delta=access_token_expires
    )

    return TokenResponse(access_token=access_token)


  