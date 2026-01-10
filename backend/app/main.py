from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.db import init_db

from app.routers.auth import router as auth_router
from app.routers.apps import router as apps_router
from app.routers.roles import router as roles_router
from app.routers.memberships import router as memberships_router
from app.routers.requests import router as requests_router
from app.routers.admin import router as admin_router
from app.core.settings import settings

app = FastAPI(title="Sentry Lite")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    app.state.settings = settings
    init_db()

@app.get("/")
def root():
    return {"message": "Welcome to Sentry Lite!"}

app.include_router(auth_router)
app.include_router(apps_router)
app.include_router(roles_router)
app.include_router(memberships_router)
app.include_router(requests_router)
app.include_router(admin_router)
  
    
