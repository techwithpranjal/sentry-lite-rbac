from datetime import datetime
from typing import List

from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel import Session

from app.schemas import RequestRead, RequestCreate, RequestUpdate
from app.queries import GET_ROLE_BY_ID, GET_REQUEST_BY_USER_ID_AND_ROLE_ID, INSERT_REQUEST, GET_REQUESTS_BY_USER_ID, GET_REQUESTS_BY_REQUEST_ID, GET_REQUESTS_BY_POC, UPDATE_REQUEST_STATUS, INSERT_MEMBERSHIP
from app.db.db import get_session
from app.core.security import get_logged_user

router = APIRouter(prefix="/requests", tags=["requests"])

@router.post("/", response_model=RequestRead, status_code=status.HTTP_200_OK)
def create_request(request: RequestCreate, session: Session = Depends(get_session), current_user: dict = Depends(get_logged_user)):
    """Create a new membership request for a role for the logged in user."""

    role_exists = session.exec(
        GET_ROLE_BY_ID.params({"role_id": request.role_id})
    ).first()

    if not role_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Role id not found."
        )

    existing_request = session.exec(
        GET_REQUEST_BY_USER_ID_AND_ROLE_ID.params({
            "user_id": int(current_user["sub"]["id"]),
            "role_id": request.role_id
        })).first()
    
    if existing_request:
        if existing_request.status == "pending":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Request is already pending."
            )
        elif existing_request.status == "approved":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Membership already approved."
            )
    
    session.exec(
        INSERT_REQUEST.params(
            {
                "user_id": current_user["sub"]["id"],
                "app_id": request.app_id,
                "role_id": request.role_id,
                "justification": request.justification,
                "created_at": datetime.utcnow()
            }
        )
    )
    session.commit()

    result = session.exec(
        GET_REQUEST_BY_USER_ID_AND_ROLE_ID.params({
            "user_id": current_user["sub"]["id"],
            "role_id": request.role_id
        })
    ).first()

    new_request = RequestRead(
        id=result.id,
        user_id=result.user_id,
        app_id=result.app_id,
        role_id=result.role_id,
        justification=result.justification,
        status=result.status,
        created_at=result.created_at,
        updated_by=result.updated_by,
        updated_at=result.updated_at
    )
    return new_request
    
@router.get("/me", response_model=List[RequestRead], status_code=status.HTTP_200_OK)
def get_my_requests(session: Session = Depends(get_session), current_user: dict = Depends(get_logged_user)):
    """Get all membership requests for the logged in user."""

    results = session.exec(
        GET_REQUESTS_BY_USER_ID.params({"user_id": current_user["sub"]["id"]})
    )
    rows = results.fetchall()

    requests = [
        RequestRead(
            id=row.id,
            user_id=row.user_id,
            app_id=row.app_id,
            role_id=row.role_id,
            justification=row.justification,
            status=row.status,
            created_at=row.created_at,
            updated_by=row.updated_by,
            updated_at=row.updated_at
        )
        for row in rows
    ]
    return requests

@router.get("/approvals", response_model=List[RequestRead], status_code=status.HTTP_200_OK)
def get_my_approvals(session: Session = Depends(get_session), current_user: dict = Depends(get_logged_user)):
    """Get all membership requests for apps the logged in user is a point of contact for."""

    #Fetch requests where the current user is the poc for the app
    
    results = session.exec(
        GET_REQUESTS_BY_POC.params({"poc_user_id": current_user["sub"]["id"]})
    )
    rows = results.fetchall()
    requests = [
        RequestRead(
            id=row.id,
            user_id=row.user_id,
            app_id=row.app_id,
            role_id=row.role_id,
            justification=row.justification,
            status=row.status,
            created_at=row.created_at,
            updated_by=row.updated_by,
            updated_at=row.updated_at
        )
        for row in rows
    ]
    return requests

@router.post("/{request_id}/update", response_model=RequestCreate, status_code=status.HTTP_200_OK)
def update_request(payload: RequestUpdate, session: Session = Depends(get_session), current_user: dict = Depends(get_logged_user)):
    """Approve or reject a membership request."""
    
    existing_req = session.exec(
        GET_REQUESTS_BY_REQUEST_ID.params({"request_id": payload.request_id})
    ).first()

    if not existing_req:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Request id not found."
        )
    
    if existing_req.status != "pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Request is already {existing_req.status}."
        )
    
    if payload.status == "approved":
        session.exec(
            INSERT_MEMBERSHIP.params(
                {
                    "user_id": existing_req.user_id,
                    "app_id": existing_req.app_id,
                    "role_id": existing_req.role_id,
                    "created_at": datetime.utcnow()
                }
            )
        )
        session.commit()

    session.exec(
        UPDATE_REQUEST_STATUS.params(
            {
                "request_id": payload.request_id,
                "status": payload.status,
                "updated_by": current_user["sub"]["id"],
                "updated_at": datetime.utcnow()
            }
        )
    )
    session.commit()

    updated_req = session.exec(
        GET_REQUESTS_BY_REQUEST_ID.params({"request_id": payload.request_id})
    ).first()

    updated_request = RequestRead(
        id=updated_req.id,
        user_id=updated_req.user_id,
        app_id=updated_req.app_id,
        role_id=updated_req.role_id,
        justification=updated_req.justification,
        status=updated_req.status,
        created_at=updated_req.created_at,
        updated_by=updated_req.updated_by,
        updated_at=updated_req.updated_at
    )
    return updated_request




    
    
