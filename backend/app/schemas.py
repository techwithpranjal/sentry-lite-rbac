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
    poc_user_id: int
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
    user_id: int
    app_id: int
    role_id: int

class MembershipRead(BaseModel):
    id: int
    user_id: int
    app_id: int
    role_id: int
    created_at: datetime
    
# ---- Request schemas ----

class RequestCreate(BaseModel):
    app_id: int
    role_id: int
    justification: Optional[str] = None

class RequestRead(BaseModel):
    id: int
    user_id: int
    app_id: int
    role_id: int
    justification: Optional[str] = None
    status: str
    created_at: datetime
    updated_by: Optional[int] = None
    updated_at: Optional[datetime] = None

class RequestUpdate(BaseModel):
    request_id: int
    status: str






