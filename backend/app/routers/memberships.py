from typing import List
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.models import User
from app.schemas import MembershipCreate, MembershipRead
from app.queries import GET_MEMBERSHIPS_BY_ROLE_ID, GET_ROLE_BY_ID, INSERT_MEMBERSHIP, GET_MEMBERSHIP_BY_USER_ID_AND_ROLE_ID, GET_MEMBERSHIPS_BY_USER_ID
from app.db.db import get_session
from app.core.security import get_logged_user


router = APIRouter(prefix="/memberships", tags=["memberships"])

@router.get("/", response_model=List[MembershipRead], status_code=status.HTTP_200_OK)
def get_memberships(role_id: int, session: Session = Depends(get_session)):
    """Retrieve the list of memberships for a role."""
    
    result = session.exec(
        GET_MEMBERSHIPS_BY_ROLE_ID.params({"role_id": role_id})
    )
    rows = result.fetchall()

    memberships = [
        MembershipRead(
            id=row.id,
            user_id=row.user_id,
            app_id=row.app_id,
            role_id=row.role_id,
            created_at=row.created_at
        )
        for row in rows
    ]
    return memberships

@router.post("/", response_model=MembershipRead, status_code=status.HTTP_201_CREATED)
def create_membership(membership: MembershipCreate, session: Session = Depends(get_session)):
    """Create a new membership for a role."""
    
    existing_role = session.exec(
        GET_ROLE_BY_ID.params({"role_id": membership.role_id})
    ).first()

    if not existing_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Role id not found."
        )
    
    existing_membership = session.exec(
        GET_MEMBERSHIP_BY_USER_ID_AND_ROLE_ID.params({
            "user_id": membership.user_id,
            "role_id": membership.role_id
        })).first()
    
    if existing_membership:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Membership already exists."
        )
    
    session.exec(
        INSERT_MEMBERSHIP.params({
            "user_id": membership.user_id,
            "app_id": membership.app_id,
            "role_id": membership.role_id,
            "created_at": datetime.utcnow()
        })
    )
    session.commit()

    result = session.exec(
        GET_MEMBERSHIP_BY_USER_ID_AND_ROLE_ID.params({
            "user_id": membership.user_id,
            "role_id": membership.role_id
        })
    ).first()

    new_membership = MembershipRead(
        id=result.id,
        user_id=result.user_id,
        app_id=result.app_id,
        role_id=result.role_id,
        created_at=result.created_at
    )
    return new_membership

@router.get("/me", response_model=List[MembershipRead], status_code=status.HTTP_200_OK)
def get_my_memberships(session: Session = Depends(get_session), current_user: User = Depends(get_logged_user)):
    """Retrieve the list of memberships for the current user."""
    
    result = session.exec(
        GET_MEMBERSHIPS_BY_USER_ID.params({"user_id": current_user['sub']['id']})
    )
    rows = result.fetchall()

    memberships = [
        MembershipRead(
            id=row.id,
            user_id=row.user_id,
            app_id=row.app_id,
            role_id=row.role_id,
            created_at=row.created_at
        )
        for row in rows
    ]
    return memberships
    

    

    


