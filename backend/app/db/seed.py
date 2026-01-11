from datetime import datetime, timedelta
from sqlmodel import Session, create_engine
from app.models import User, App, Role, Membership, Request
from app.queries import (
    TRUNCATE_USER_TABLE,
    TRUNCATE_APP_TABLE,
    TRUNCATE_ROLE_TABLE,
    TRUNCATE_MEMBERSHIP_TABLE,
    TRUNCATE_REQUEST_TABLE,
)
from app.core.security import hash_password

DATABASE_URL = "sqlite:///db/sentry_lite.db"
engine = create_engine(DATABASE_URL, echo=False)


def seed(session: Session = None):
        
        session.exec(TRUNCATE_REQUEST_TABLE)
        session.exec(TRUNCATE_MEMBERSHIP_TABLE)
        session.exec(TRUNCATE_ROLE_TABLE)
        session.exec(TRUNCATE_APP_TABLE)
        session.exec(TRUNCATE_USER_TABLE)
        session.commit()

        # USERS 

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

        user_map = {u.email: u for u in users}

        # APPLICATIONS 

        apps = [
            App(
                name="LTX",
                slug="ltx",
                description="Lifetime Value Experiments",
                poc_user_email="admin@sentry.io",
            ),
            App(
                name="Pulse",
                slug="pulse",
                description="Customer Sentiment Analytics",
                poc_user_email="alice@corp.com",
            ),
            App(
                name="Nova",
                slug="nova",
                description="A/B Experiment Platform",
                poc_user_email="bob@corp.com",
            ),
            App(
                name="Atlas",
                slug="atlas",
                description="Enterprise Reporting Suite",
                poc_user_email="charlie@corp.com",
            ),
            App(
                name="Beacon",
                slug="beacon",
                description="Observability & Alerts",
                poc_user_email="admin@sentry.io",
            ),
        ]

        session.add_all(apps)
        session.commit()

        app_map = {a.slug: a for a in apps}

        # ROLES 

        roles = [
            # LTX
            Role(app_id=app_map["ltx"].id, name="admin", description="Full control"),
            Role(app_id=app_map["ltx"].id, name="analyst", description="View dashboards"),
            Role(app_id=app_map["ltx"].id, name="experimenter", description="Run tests"),

            # Pulse
            Role(app_id=app_map["pulse"].id, name="owner", description="App owner"),
            Role(app_id=app_map["pulse"].id, name="viewer", description="Read-only"),
            Role(app_id=app_map["pulse"].id, name="editor", description="Edit configs"),

            # Nova
            Role(app_id=app_map["nova"].id, name="admin", description="Admin access"),
            Role(app_id=app_map["nova"].id, name="scientist", description="Model training"),
            Role(app_id=app_map["nova"].id, name="viewer", description="View results"),

            # Atlas
            Role(app_id=app_map["atlas"].id, name="admin", description="Manage reports"),
            Role(app_id=app_map["atlas"].id, name="publisher", description="Publish"),
            Role(app_id=app_map["atlas"].id, name="viewer", description="View only"),

            # Beacon
            Role(app_id=app_map["beacon"].id, name="admin", description="Alert admin"),
            Role(app_id=app_map["beacon"].id, name="oncall", description="On-call engineer"),
            Role(app_id=app_map["beacon"].id, name="viewer", description="View alerts"),
        ]

        session.add_all(roles)
        session.commit()

        role_map = {(r.app_id, r.name): r for r in roles}

        # MEMBERSHIPS 

        memberships = [
            # LTX
            Membership(
                user_email="alice@corp.com",
                app_id=app_map["ltx"].id,
                role_id=role_map[(app_map["ltx"].id, "analyst")].id,
                created_by="admin@sentry.io",
            ),
            Membership(
                user_email="bob@corp.com",
                app_id=app_map["ltx"].id,
                role_id=role_map[(app_map["ltx"].id, "experimenter")].id,
                created_by="admin@sentry.io",
            ),

            # Pulse
            Membership(
                user_email="charlie@corp.com",
                app_id=app_map["pulse"].id,
                role_id=role_map[(app_map["pulse"].id, "editor")].id,
                created_by="alice@corp.com",
            ),
            Membership(
                user_email="emma@corp.com",
                app_id=app_map["pulse"].id,
                role_id=role_map[(app_map["pulse"].id, "viewer")].id,
                created_by="alice@corp.com",
            ),

            # Nova
            Membership(
                user_email="frank@corp.com",
                app_id=app_map["nova"].id,
                role_id=role_map[(app_map["nova"].id, "scientist")].id,
                created_by="bob@corp.com",
            ),

            # Atlas
            Membership(
                user_email="grace@corp.com",
                app_id=app_map["atlas"].id,
                role_id=role_map[(app_map["atlas"].id, "viewer")].id,
                created_by="charlie@corp.com",
            ),

            # Beacon
            Membership(
                user_email="henry@corp.com",
                app_id=app_map["beacon"].id,
                role_id=role_map[(app_map["beacon"].id, "oncall")].id,
                created_by="admin@sentry.io",
            ),
        ]

        session.add_all(memberships)
        session.commit()

        # REQUESTS 

        requests = [
            # Pending
            Request(
                user_email=user_map["ivy@corp.com"].email,
                app_id=app_map["ltx"].id,
                role_id=role_map[(app_map["ltx"].id, "analyst")].id,
                justification="Need access for reporting",
            ),

            # Approved
            Request(
                user_email=user_map["david@corp.com"].email,
                app_id=app_map["pulse"].id,
                role_id=role_map[(app_map["pulse"].id, "viewer")].id,
                status="approved",
                updated_by="alice@corp.com",
                updated_at=datetime.utcnow() - timedelta(days=1),
            ),

            # Rejected
            Request(
                user_email=user_map["emma@corp.com"].email,
                app_id=app_map["nova"].id,
                role_id=role_map[(app_map["nova"].id, "admin")].id,
                status="rejected",
                updated_by="bob@corp.com",
                updated_at=datetime.utcnow() - timedelta(days=2),
            ),

            # Another pending
            Request(
                user_email=user_map["frank@corp.com"].email,
                app_id=app_map["atlas"].id,
                role_id=role_map[(app_map["atlas"].id, "publisher")].id,
                justification="Publishing reports",
            ),
        ]

        session.add_all(requests)
        session.commit()


if __name__ == "__main__":
    seed()