from fastapi import FastAPI
from app.db import init_db
from app.routers.auth import router as auth_router
from app.routers.apps import router as apps_router
from app.routers.roles import router as roles_router
from app.core.settings import settings

app = FastAPI(title="Sentry Lite")

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
  
    
