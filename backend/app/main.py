from fastapi import FastAPI
from app.db import init_db
from app.routers.auth import router as auth_router

app = FastAPI(title="Sentry Lite")

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/")
def root():
    return {"message": "Welcome to Sentry Lite!"}

app.include_router(auth_router)
  
    
