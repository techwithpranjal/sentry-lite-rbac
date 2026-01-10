from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing import List

from app.core.security import require_admin
from app.db.db import get_session
from app.schemas import (
    AdminOverview,
    AdminAppRead,
    AdminRoleRead,
    AdminRequestRead,
    AdminMembershipRead,
)
from app.queries import (
    ADMIN_OVERVIEW,
    ADMIN_APPS,
    ADMIN_ROLES,
    ADMIN_REQUESTS,
    ADMIN_MEMBERSHIPS,
)

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/overview", response_model=AdminOverview)
def admin_overview(
    session: Session = Depends(get_session),
    _: dict = Depends(require_admin),
):
    row = session.exec(ADMIN_OVERVIEW).first()
    return AdminOverview(**row._mapping)


@router.get("/apps", response_model=List[AdminAppRead])
def admin_apps(
    session: Session = Depends(get_session),
    _: dict = Depends(require_admin),
):
    rows = session.exec(ADMIN_APPS).fetchall()
    return [AdminAppRead(**r._mapping) for r in rows]

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


@router.get("/memberships", response_model=List[AdminMembershipRead])
def admin_memberships(
    session: Session = Depends(get_session),
    _: dict = Depends(require_admin),
):
    rows = session.exec(ADMIN_MEMBERSHIPS).fetchall()
    return [AdminMembershipRead(**r._mapping) for r in rows]


