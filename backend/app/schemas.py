from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# ---- User schemas ----

class UserRegister(BaseModel):
    email: EmailStr
    password: str

class UserRead(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    is_super_admin: bool

# ---- Auth schemas ----

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class IdentityRead(BaseModel):
    user: dict
    owned_apps: list
    memberships: list
    requests: list

# ---- App schemas ----

class AppCreate(BaseModel):
    name: str
    slug: str
    description: str

class AppRead(BaseModel):
    id: int
    name: str
    slug: str
    description: str
    poc_user_email: str
    created_at: datetime

# ---- Role schemas ----

class RoleCreate(BaseModel):
    app_id: int
    name: str
    description: str

class RoleRead(BaseModel):
    id: int
    app_id: int
    name: str
    description: str
    created_at: datetime

# ---- Membership schemas ----

class MembershipCreate(BaseModel):
    user_email: str
    app_id: int
    role_id: int
    created_by: Optional[str] = None

class MembershipRead(BaseModel):
    id: int
    user_email: str
    app_id: int
    app_name: str
    role_id: int
    role_name: str
    created_at: datetime
    created_by: Optional[str] = None
    
# ---- Request schemas ----

class RequestCreate(BaseModel):
    app_id: int
    role_id: int
    justification: Optional[str] = None

class RequestRead(BaseModel):
    id: int
    user_email: str
    app_id: int
    app_name: str
    role_id: int
    role_name: str
    justification: Optional[str] = None
    status: str
    created_at: datetime
    updated_by: Optional[str] = None
    updated_at: Optional[datetime] = None

class RequestUpdate(BaseModel):
    request_id: int
    status: str

# ---- Admin schema ----

class AdminStats(BaseModel):
    users: int
    applications: int
    roles: int
    memberships: int
    pendingRequests: int

    appsWithoutOwner: int
    rolesWithoutMembers: int
    oldestPendingRequestDays: Optional[int]

    requestsLast24h: int
    approvalsLast24h: int
    membershipsLast24h: int
    appsLast7d: int

class AdminOverview(BaseModel):
    stats: AdminStats
    pending_requests: list

class AdminRoleRead(BaseModel):
    role_id: int
    role_name: str
    app_name: str
    app_slug: str
    members_count: int
    created_at: datetime

class AdminRequestRead(BaseModel):
    request_id: int
    user_email: str
    app_name: str
    role_name: str
    status: str
    justification: Optional[str]
    created_at: datetime
    updated_by: Optional[str]
    updated_at: Optional[datetime]






