from datetime import datetime, timedelta
from sqlmodel import Session
from app.models import User, App, Role, Membership, Request
from app.queries import (
    TRUNCATE_USER_TABLE,
    TRUNCATE_APP_TABLE,
    TRUNCATE_ROLE_TABLE,
    TRUNCATE_MEMBERSHIP_TABLE,
    TRUNCATE_REQUEST_TABLE,
)
from app.core.security import hash_password


def seed(session: Session):

    session.exec(TRUNCATE_REQUEST_TABLE)
    session.exec(TRUNCATE_MEMBERSHIP_TABLE)
    session.exec(TRUNCATE_ROLE_TABLE)
    session.exec(TRUNCATE_APP_TABLE)
    session.exec(TRUNCATE_USER_TABLE)
    session.commit()

    users = [
        User(email="admin@sentry.io", password_hash=hash_password("admin123"), is_super_admin=True),
        User(email="alice@corp.com", password_hash=hash_password("password")),
        User(email="bob@corp.com", password_hash=hash_password("password")),
        User(email="charlie@corp.com", password_hash=hash_password("password")),
        User(email="david@corp.com", password_hash=hash_password("password")),
        User(email="emma@corp.com", password_hash=hash_password("password")),
        User(email="frank@corp.com", password_hash=hash_password("password")),
        User(email="grace@corp.com", password_hash=hash_password("password")),
        User(email="henry@corp.com", password_hash=hash_password("password")),
        User(email="ivy@corp.com", password_hash=hash_password("password")),
    ]

    session.add_all(users)
    session.commit()

    apps = [
        App(name="Revenue Analysis", slug="revenue-analysis", description="Revenue dashboards", poc_user_email="alice@corp.com"),
        App(name="Customer Insights", slug="customer-insights", description="Customer analytics", poc_user_email="charlie@corp.com"),
        App(name="Design Factory", slug="design-factory", description="Design tooling", poc_user_email="grace@corp.com"),
        App(name="Access Audit Tool", slug="access-audit", description="Compliance audits", poc_user_email="david@corp.com"),
        App(name="Operations Console", slug="operations-console", description="Internal ops", poc_user_email="bob@corp.com"),
    ]

    session.add_all(apps)
    session.commit()

    app_map = {a.slug: a for a in apps}

    roles = [
        Role(app_id=app_map["revenue-analysis"].id, name="Admin"),
        Role(app_id=app_map["revenue-analysis"].id, name="Editor"),
        Role(app_id=app_map["revenue-analysis"].id, name="Analyst"),
        Role(app_id=app_map["revenue-analysis"].id, name="Auditor"),

        Role(app_id=app_map["customer-insights"].id, name="Admin"),
        Role(app_id=app_map["customer-insights"].id, name="Analyst"),
        Role(app_id=app_map["customer-insights"].id, name="Viewer"),

        Role(app_id=app_map["design-factory"].id, name="Admin"),
        Role(app_id=app_map["design-factory"].id, name="Designer"),
        Role(app_id=app_map["design-factory"].id, name="Viewer"),

        Role(app_id=app_map["access-audit"].id, name="Admin"),
        Role(app_id=app_map["access-audit"].id, name="Auditor"),

        Role(app_id=app_map["operations-console"].id, name="Admin"),
        Role(app_id=app_map["operations-console"].id, name="Support"),
        Role(app_id=app_map["operations-console"].id, name="Viewer"),
    ]

    session.add_all(roles)
    session.commit()

    role_map = {(r.app_id, r.name): r for r in roles}

    memberships = [
        Membership(user_email="alice@corp.com", app_id=app_map["revenue-analysis"].id,
                   role_id=role_map[(app_map["revenue-analysis"].id, "Admin")].id, created_by="admin@sentry.io"),

        Membership(user_email="emma@corp.com", app_id=app_map["revenue-analysis"].id,
                   role_id=role_map[(app_map["revenue-analysis"].id, "Analyst")].id, created_by="alice@corp.com"),

        Membership(user_email="charlie@corp.com", app_id=app_map["customer-insights"].id,
                   role_id=role_map[(app_map["customer-insights"].id, "Admin")].id, created_by="admin@sentry.io"),

        Membership(user_email="grace@corp.com", app_id=app_map["design-factory"].id,
                   role_id=role_map[(app_map["design-factory"].id, "Admin")].id, created_by="admin@sentry.io"),

        Membership(user_email="david@corp.com", app_id=app_map["access-audit"].id,
                   role_id=role_map[(app_map["access-audit"].id, "Admin")].id, created_by="admin@sentry.io"),

        Membership(user_email="bob@corp.com", app_id=app_map["operations-console"].id,
                   role_id=role_map[(app_map["operations-console"].id, "Admin")].id, created_by="admin@sentry.io"),
    ]

    session.add_all(memberships)
    session.commit()

    requests = [
        Request(user_email="frank@corp.com", app_id=app_map["revenue-analysis"].id,
                role_id=role_map[(app_map["revenue-analysis"].id, "Auditor")].id,
                justification="Quarterly audit"),

        Request(user_email="ivy@corp.com", app_id=app_map["design-factory"].id,
                role_id=role_map[(app_map["design-factory"].id, "Designer")].id,
                justification="Design work"),

        Request(user_email="emma@corp.com", app_id=app_map["operations-console"].id,
                role_id=role_map[(app_map["operations-console"].id, "Viewer")].id,
                status="approved", updated_by="bob@corp.com",
                updated_at=datetime.utcnow() - timedelta(days=1)),
    ]

    session.add_all(requests)
    session.commit()