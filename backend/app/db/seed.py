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
        App(
            name="Revenue Analysis",
            slug="revenue-analysis",
            description="Revenue dashboards and forecasting",
            poc_user_email="alice@corp.com",
        ),
        App(
            name="Customer Insights",
            slug="customer-insights",
            description="Customer behavior and segmentation",
            poc_user_email="charlie@corp.com",
        ),
        App(
            name="Design Factory",
            slug="design-factory",
            description="Design systems and asset management",
            poc_user_email="grace@corp.com",
        ),
        App(
            name="Access Audit Tool",
            slug="access-audit",
            description="Audit logs and compliance reviews",
            poc_user_email="david@corp.com",
        ),
        App(
            name="Operations Console",
            slug="operations-console",
            description="Internal ops and support tooling",
            poc_user_email="bob@corp.com",
        ),
    ]

    session.add_all(apps)
    session.commit()

    app_map = {a.slug: a for a in apps}

    roles = [
        Role(app_id=app_map["revenue-analysis"].id, name="Admin", description="Full access"),
        Role(app_id=app_map["revenue-analysis"].id, name="Editor", description="Edit dashboards"),
        Role(app_id=app_map["revenue-analysis"].id, name="Analyst", description="View reports"),
        Role(app_id=app_map["revenue-analysis"].id, name="Auditor", description="Read-only audit"),

        Role(app_id=app_map["customer-insights"].id, name="Admin", description="Manage app"),
        Role(app_id=app_map["customer-insights"].id, name="Analyst", description="Analyze data"),
        Role(app_id=app_map["customer-insights"].id, name="Viewer", description="Read-only"),
        Role(app_id=app_map["customer-insights"].id, name="Auditor", description="Compliance access"),

        Role(app_id=app_map["design-factory"].id, name="Admin", description="Design admin"),
        Role(app_id=app_map["design-factory"].id, name="Designer", description="Create assets"),
        Role(app_id=app_map["design-factory"].id, name="Viewer", description="View designs"),

        Role(app_id=app_map["access-audit"].id, name="Admin", description="Audit admin"),
        Role(app_id=app_map["access-audit"].id, name="Auditor", description="Perform audits"),
        Role(app_id=app_map["access-audit"].id, name="Viewer", description="View logs"),

        Role(app_id=app_map["operations-console"].id, name="Admin", description="Ops admin"),
        Role(app_id=app_map["operations-console"].id, name="Support", description="Handle tickets"),
        Role(app_id=app_map["operations-console"].id, name="Viewer", description="Read-only"),
    ]

    session.add_all(roles)
    session.commit()

    role_map = {(r.app_id, r.name): r for r in roles}

    memberships = [
        Membership("alice@corp.com", app_map["revenue-analysis"].id, role_map[(app_map["revenue-analysis"].id, "Admin")].id, "admin@sentry.io"),
        Membership("emma@corp.com", app_map["revenue-analysis"].id, role_map[(app_map["revenue-analysis"].id, "Analyst")].id, "alice@corp.com"),
        Membership("ivy@corp.com", app_map["revenue-analysis"].id, role_map[(app_map["revenue-analysis"].id, "Viewer")].id, "alice@corp.com"),

        Membership("charlie@corp.com", app_map["customer-insights"].id, role_map[(app_map["customer-insights"].id, "Admin")].id, "admin@sentry.io"),
        Membership("emma@corp.com", app_map["customer-insights"].id, role_map[(app_map["customer-insights"].id, "Analyst")].id, "charlie@corp.com"),

        Membership("grace@corp.com", app_map["design-factory"].id, role_map[(app_map["design-factory"].id, "Admin")].id, "admin@sentry.io"),
        Membership("charlie@corp.com", app_map["design-factory"].id, role_map[(app_map["design-factory"].id, "Viewer")].id, "grace@corp.com"),

        Membership("david@corp.com", app_map["access-audit"].id, role_map[(app_map["access-audit"].id, "Admin")].id, "admin@sentry.io"),
        Membership("frank@corp.com", app_map["access-audit"].id, role_map[(app_map["access-audit"].id, "Auditor")].id, "david@corp.com"),

        Membership("bob@corp.com", app_map["operations-console"].id, role_map[(app_map["operations-console"].id, "Admin")].id, "admin@sentry.io"),
        Membership("henry@corp.com", app_map["operations-console"].id, role_map[(app_map["operations-console"].id, "Support")].id, "bob@corp.com"),
    ]

    session.add_all(memberships)
    session.commit()

    requests = [
        Request(
            user_email="frank@corp.com",
            app_id=app_map["revenue-analysis"].id,
            role_id=role_map[(app_map["revenue-analysis"].id, "Auditor")].id,
            justification="Quarterly finance audit",
        ),
        Request(
            user_email="grace@corp.com",
            app_id=app_map["customer-insights"].id,
            role_id=role_map[(app_map["customer-insights"].id, "Viewer")].id,
            justification="Design review collaboration",
        ),
        Request(
            user_email="emma@corp.com",
            app_id=app_map["operations-console"].id,
            role_id=role_map[(app_map["operations-console"].id, "Viewer")].id,
            status="approved",
            updated_by="bob@corp.com",
            updated_at=datetime.utcnow() - timedelta(days=1),
        ),
        Request(
            user_email="ivy@corp.com",
            app_id=app_map["design-factory"].id,
            role_id=role_map[(app_map["design-factory"].id, "Designer")].id,
            status="rejected",
            updated_by="grace@corp.com",
            updated_at=datetime.utcnow() - timedelta(days=2),
        ),
    ]

    session.add_all(requests)
    session.commit()