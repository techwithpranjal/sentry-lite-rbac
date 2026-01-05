from app.models import User
from app.core.security import hash_password, verify_password, create_access_token, get_logged_user
from app.schemas import UserRegister, UserRead, LoginRequest, TokenResponse, IdentityRead
from app.db import get_session
from app.queries import GET_USER_BY_EMAIL, INSERT_USER, GET_OWNED_APPS_BY_USER_ID, GET_MEMBERSHIPS_BY_USER_ID, GET_REQUESTS_BY_USER_ID
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
        data={
            "id": str(user.id),       
            "email": user.email        
        },
        expires_delta=access_token_expires,
    )

    return TokenResponse(access_token=access_token)


@router.get("/identity", response_model=IdentityRead, status_code=status.HTTP_200_OK)
def get_identity(session: Session = Depends(get_session), current_user: dict = Depends(get_logged_user)):
    """Aggregated identity endpoint.
    Returns user info, owned apps, memberships, and pending requests.
    """

    user_data = {
        "id": current_user["sub"]["id"],
        "email": current_user["sub"]["email"]
    }

    owned_apps_result = session.exec(
        GET_OWNED_APPS_BY_USER_ID.params({"user_id": current_user["sub"]["id"]})
    ).fetchall()
    
    owned_apps = [
        {
            "id": app.id,
            "name": app.name,
            "slug": app.slug,
            "description": app.description,
            "poc_user_id": app.poc_user_id,
            "created_at": app.created_at
        }
        for app in owned_apps_result
    ]

    memberships_results = session.exec(
        GET_MEMBERSHIPS_BY_USER_ID.params({"user_id": current_user["sub"]["id"]})
    ).fetchall()

    memberships = [
        {
            "id": membership.id,
            "role_id": membership.role_id,
            "app_id": membership.app_id,
            "user_id": membership.user_id,
            "created_at": membership.created_at
        }
        for membership in memberships_results
    ]

    requests_result = session.exec(
        GET_REQUESTS_BY_USER_ID.params({"user_id": current_user["sub"]["id"]})
    ).fetchall()

    requests = [
        {
            "id": req.id,
            "user_id": req.user_id,
            "app_id": req.app_id,
            "role_id": req.role_id,
            "justification": req.justification,
            "status": req.status,
            "created_at": req.created_at
        }
        for req in requests_result
    ]

    return IdentityRead(
        user=user_data,
        owned_apps=owned_apps,
        memberships=memberships,
        requests=requests
    )


