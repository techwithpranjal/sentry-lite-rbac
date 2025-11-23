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

# ---- App schemas ----

class AppCreate(BaseModel):
    name: str
    slug: str
    description: str
    poc_user_id: int

class AppRead(BaseModel):
    id: int
    name: str
    slug: str
    description: str
    poc_user_id: int
    created_at: datetime






