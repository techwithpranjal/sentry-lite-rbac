from datetime import datetime
from sqlmodel import Session, select
from app.models import User, App, Membership
from app.core.security import hash_password

def seed_db(session: Session):
    # --- User ---
    user = session.exec(
        select(User).where(User.email == "demo@sentry.dev")
    ).first()

    if not user:
        user = User(
            email="demo@sentry.dev",
            password_hash=hash_password("demo123"),
            created_at=datetime.utcnow()
        )
        session.add(user)
        session.commit()
        session.refresh(user)