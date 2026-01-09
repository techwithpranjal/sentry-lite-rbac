from typing import List
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.models import User
from app.schemas import MembershipCreate, MembershipRead
from app.queries import GET_MEMBERSHIPS_BY_ROLE_ID, CHECK_IF_USER_IS_APP_OWNER, GET_ROLE_BY_ID, GET_USER_BY_EMAIL, INSERT_MEMBERSHIP, GET_MEMBERSHIP_BY_USER_EMAIL_AND_ROLE_ID, GET_MEMBERSHIP_BY_ID, GET_MEMBERSHIPS_BY_USER_EMAIL, DELETE_MEMBERSHIP_BY_ID
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
            user_email=row.user_email,
            app_id=row.app_id,
            app_name=row.app_name,
            role_id=row.role_id,
            role_name=row.role_name,
            created_at=row.created_at,
            created_by=row.created_by
        )
        for row in rows
    ]
    return memberships

@router.post("/", response_model=MembershipRead, status_code=status.HTTP_201_CREATED)
def create_membership(membership: MembershipCreate, session: Session = Depends(get_session), current_user: dict = Depends(get_logged_user)):
    """Create a new membership for a role."""
    
    existing_role = session.exec(
        GET_ROLE_BY_ID.params({"role_id": membership.role_id})
    ).first()

    if not existing_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Role id not found."
        )
    
    owner = session.exec(
        CHECK_IF_USER_IS_APP_OWNER.params({"app_id": membership.app_id, "poc_user_email": current_user['sub']['email']})
    ).first()

    if not owner:
        raise HTTPException(
            status_code=403,
            detail="Only app owners can add members"
        )
    
    existing_membership = session.exec(
        GET_MEMBERSHIP_BY_USER_EMAIL_AND_ROLE_ID.params({
            "user_email": membership.user_email,
            "role_id": membership.role_id
        })).first()
    
    if existing_membership:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Membership already exists."
        )
    
    existing_user = session.exec(
        GET_USER_BY_EMAIL.params({
            "email": membership.user_email
        })
    ).first()

    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist"
        )
    
    session.exec(
        INSERT_MEMBERSHIP.params({
            "user_email": membership.user_email,
            "app_id": membership.app_id,
            "role_id": membership.role_id,
            "created_at": datetime.utcnow(),
            "created_by": current_user['sub']['email']
        })
    )
    session.commit()

    result = session.exec(
        GET_MEMBERSHIP_BY_USER_EMAIL_AND_ROLE_ID.params({
            "user_email": membership.user_email,
            "role_id": membership.role_id
        })
    ).first()

    new_membership = MembershipRead(
        id=result.id,
        user_email=result.user_email,
        app_id=result.app_id,
        app_name=result.app_name,
        role_id=result.role_id,
        role_name=result.role_name,
        created_at=result.created_at,
        created_by=result.created_by
    )
    return new_membership

@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_membership(membership_id: int, session: Session = Depends(get_session)):
    """Delete a membership by its ID."""
    
    existing_membership = session.exec(
        GET_MEMBERSHIP_BY_ID.params({
            "id": membership_id
        })
    ).first()

    if not existing_membership:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Membership not found"
        )
    
    session.exec(
        DELETE_MEMBERSHIP_BY_ID.params({"id": membership_id})
    )
    session.commit()
    return

@router.get("/me", response_model=List[MembershipRead], status_code=status.HTTP_200_OK)
def get_my_memberships(session: Session = Depends(get_session), current_user: User = Depends(get_logged_user)):
    """Retrieve the list of memberships for the current user."""
    
    result = session.exec(
        GET_MEMBERSHIPS_BY_USER_EMAIL.params({"user_email": current_user['sub']['email']})
    )
    rows = result.fetchall()

    memberships = [
        MembershipRead(
            id=row.id,
            user_email=row.user_email,
            app_id=row.app_id,
            app_name=row.app_name,
            role_id=row.role_id,
            role_name=row.role_name,
            created_at=row.created_at,
            created_by=row.created_by
        )
        for row in rows
    ]
    return memberships
    

    

    


