from app.models import User
from app.security import hash_password, verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from app.schemas import UserRegister, UserRead, LoginRequest, TokenResponse
from app.db import get_session
from app.queries import GET_USER_BY_EMAIL

from datetime import timedelta

from sqlmodel import Session
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register_user(user: UserRegister, session: Session = Depends(get_session)):
    # Check if user already exists
    result = session.exec(GET_USER_BY_EMAIL, {"email": user.email})
    existing_user = result.first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        email = user.email,
        password_hash = hash_password(user.password)   
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return UserRead(
        id=user.id,
        email=user.email,
        created_at=user.created_at
    )

@router.post("/login", response_model=TokenResponse)
def login_user(login_req: LoginRequest, session: Session = Depends(get_session)):
    
    result = session.exec(GET_USER_BY_EMAIL, {"email": login_req.email})
    user = result.first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email or password.")

    if not verify_password(login_req.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email or password.")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email},
        expires_delta=access_token_expires
    )

    return TokenResponse(access_token=access_token)


  