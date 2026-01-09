from typing import List
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.schemas import AppCreate, AppRead
from app.queries import GET_APPS, GET_APP_BY_SLUG, INSERT_APP
from app.db.db import get_session
from app.core.security import get_logged_user


router = APIRouter(prefix="/apps", tags=["apps"])

@router.get("/", response_model=List[AppRead], status_code=status.HTTP_200_OK)
def get_apps(session: Session = Depends(get_session)):
    """Retrieve the list of registered applications."""
    
    result = session.exec(GET_APPS)
    rows = result.fetchall()

    apps = [
        AppRead(
            id=row.id,
            name=row.name,
            slug=row.slug,
            description=row.description,
            poc_user_email=row.poc_user_email,
            created_at=row.created_at
        )
        for row in rows
    ]
    return apps


@router.post("/", response_model=AppRead, status_code=status.HTTP_201_CREATED)
def create_app(app: AppCreate, session: Session = Depends(get_session), current_user: dict = Depends(get_logged_user)):
    """Register a new application."""

    existing_app = session.exec(GET_APP_BY_SLUG.params({"slug": app.slug})).first()
    
    if existing_app:
        raise HTTPException(status_code=400, detail="App with this slug already exists")

    session.exec(
        INSERT_APP.params(
            {
                "name": app.name,
                "slug": app.slug,
                "description": app.description,
                "poc_user_email": current_user["sub"]["email"],
                "created_at": datetime.utcnow()
            }
        )
    )
    session.commit()

    result = session.exec(GET_APP_BY_SLUG.params({"slug": app.slug}))
    row = result.first()

    new_app = AppRead(
        id=row.id,
        name=row.name,
        slug=row.slug,
        description=row.description,
        poc_user_email=row.poc_user_email,
        created_at=row.created_at
    )
    return new_app

