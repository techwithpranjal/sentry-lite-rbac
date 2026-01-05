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

    # --- App ---
    app = session.exec(
        select(App).where(App.slug == "billing")
    ).first()

    if not app:
        app = App(
            name="Billing",
            slug="billing",
            description="Billing platform",
            poc_user_id=user.id,
        )
        session.add(app)
        session.commit()
        session.refresh(app)

    # --- Membership ---
    membership = session.exec(
        select(Membership).where(
            Membership.user_id == user.id,
            Membership.app_id == app.id
        )
    ).first()

    if not membership:
        membership = Membership(
            user_id=user.id,
            app_id=app.id,
            role_id=1
        )
        session.add(membership)
        session.commit()