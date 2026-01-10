from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing import List

from app.core.security import require_admin
from app.db.db import get_session
from app.schemas import (
    AdminOverview,
    AppRead,
    AdminRoleRead,
    AdminRequestRead,
    MembershipRead,
)
from app.queries import (
    ADMIN_OVERVIEW,
    ADMIN_APPS,
    ADMIN_ROLES,
    ADMIN_REQUESTS,
    ADMIN_MEMBERSHIPS,
    GET_PENDING_REQUESTS
)

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/overview", response_model=AdminOverview)
def get_admin_overview(
    session: Session = Depends(get_session),
    _: dict = Depends(require_admin),
):
    row = session.exec(ADMIN_OVERVIEW).first()
    stats = {
        "users": row.users,
        "applications": row.applications,
        "roles": row.roles,
        "memberships": row.memberships,
        "pendingRequests": row.pending_requests,
        "appsWithoutOwner": row.apps_without_owner,
        "rolesWithoutMembers": row.roles_without_members,
        "oldestPendingRequestDays": row.oldest_pending_request_days,
        "requestsLast24h": row.requests_last_24h,
        "approvalsLast24h": row.approvals_last_24h,
        "membershipsLast24h": row.memberships_last_24h,
        "appsLast7d": row.apps_last_7d,
    }

    pending_rows = session.exec(GET_PENDING_REQUESTS).fetchall()
    pending_requests = [
        {
            "id": r.id,
            "user_email": r.user_email,
            "app_name": r.app_name,
            "role_name": r.role_name,
            "status": r.status,
            "created_at": r.created_at,
        }
        for r in pending_rows
    ]

    return AdminOverview(
            stats=stats,
            pending_requests=pending_requests,
        )
    

@router.get("/apps", response_model=List[AppRead])
def admin_apps(
    session: Session = Depends(get_session),
    _: dict = Depends(require_admin),
):
    rows = session.exec(ADMIN_APPS).fetchall()
    return [AppRead(**r._mapping) for r in rows]

@router.get("/roles", response_model=List[AdminRoleRead])
def admin_roles(
    session: Session = Depends(get_session),
    _: dict = Depends(require_admin),
):
    rows = session.exec(ADMIN_ROLES).fetchall()
    return [AdminRoleRead(**r._mapping) for r in rows]

@router.get("/requests", response_model=List[AdminRequestRead])
def admin_requests(
    session: Session = Depends(get_session),
    _: dict = Depends(require_admin),
):
    rows = session.exec(ADMIN_REQUESTS).fetchall()
    return [AdminRequestRead(**r._mapping) for r in rows]


@router.get("/memberships", response_model=List[MembershipRead])
def admin_memberships(
    session: Session = Depends(get_session),
    _: dict = Depends(require_admin),
):
    rows = session.exec(ADMIN_MEMBERSHIPS).fetchall()
    return [MembershipRead(**r._mapping) for r in rows]


