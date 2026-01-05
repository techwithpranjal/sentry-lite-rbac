from typing import List
from datetime import datetime

from fastapi import APIRouter, status, Depends, HTTPException
from sqlmodel import Session

from app.schemas import RoleRead, RoleCreate
from app.db.db import get_session
from app.queries import GET_ROLES_BY_APP_ID, GET_ROLE_BY_NAME_AND_APP_ID, GET_APP_BY_APP_ID, INSERT_ROLE



router =  APIRouter(prefix="/roles", tags=["roles"])

@router.get("/", response_model=List[RoleRead], status_code=status.HTTP_200_OK)
def get_roles(app_id: int, session: Session = Depends(get_session)):
    """Retrieve the list of available roles for an application."""
    
    result = session.exec(GET_ROLES_BY_APP_ID.params({"app_id": app_id}))
    rows = result.fetchall()

    roles = [
        RoleRead(
            id=row.id,
            app_id=row.app_id,
            name=row.name,
            description=row.description,
            created_at=row.created_at
        ) for row in rows
    ]
    return roles

@router.post("/", response_model=RoleRead, status_code=status.HTTP_201_CREATED)
def create_role(role: RoleCreate, session: Session = Depends(get_session)):
    """Create a new role for an application."""

    existing_app = session.exec(
        GET_APP_BY_APP_ID.params({"app_id": role.app_id})
    ).first()

    if not existing_app:
        raise HTTPException(status_code=404, detail="Application not found.")

    existing_role = session.exec(
        GET_ROLE_BY_NAME_AND_APP_ID.params({"name": role.name, "app_id": role.app_id})
    ).first()

    if existing_role:
        raise HTTPException(status_code=400, detail="Role with this name already exists for the application.")
    
    session.exec(
        INSERT_ROLE.params({
            "app_id": role.app_id,
            "name": role.name,
            "description": role.description,
            "created_at": datetime.utcnow()
        })
    )
    session.commit()

    row = session.exec(
        GET_ROLE_BY_NAME_AND_APP_ID.params({"name": role.name, "app_id": role.app_id})
    ).first()

    new_role = RoleRead(
        id=row.id,
        app_id=row.app_id,
        name=row.name,
        description=row.description,
        created_at=row.created_at
    )
    return new_role



    