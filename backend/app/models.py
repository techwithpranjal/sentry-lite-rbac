from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True)
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class App(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    slug: str
    description: str
    poc_user_email: int = Field(foreign_key="user.email")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    

class Role(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    app_id: int = Field(foreign_key="app.id")
    name: str
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Membership(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    app_id: int = Field(foreign_key="app.id")
    role_id: int = Field(foreign_key="role.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Request(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    app_id: int = Field(foreign_key="app.id")
    role_id: int = Field(foreign_key="role.id")
    status: str = Field(default="pending") 
    justification: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_by: Optional[int] = Field(default=None, foreign_key="user.id")
    updated_at: Optional[datetime] = None

    