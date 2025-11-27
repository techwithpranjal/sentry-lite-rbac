from sqlalchemy import text

# User Queries

GET_USER_BY_EMAIL = text("""
    SELECT * FROM user WHERE email = :email
""")

INSERT_USER = text("""
    INSERT INTO user (email, password_hash, created_at) VALUES (:email, :password_hash, :created_at)
""")

# App Queries

GET_APPS = text("""
    SELECT id, name, slug, description, poc_user_id, created_at FROM app ORDER BY created_at DESC
""")

GET_APP_BY_APP_ID = text("""
    SELECT * FROM app WHERE id = :app_id
""")

GET_APP_BY_SLUG = text("""
    SELECT * FROM app WHERE slug = :slug
""")

INSERT_APP = text("""
    INSERT INTO app (name, slug, description, poc_user_id, created_at)
    VALUES (:name, :slug, :description, :poc_user_id, :created_at)
""")

# Role Queries

GET_ROLES_BY_APP_ID = text("""
    SELECT id, app_id, name, description, created_at FROM role WHERE app_id = :app_id ORDER BY created_at DESC
""")

GET_ROLE_BY_NAME_AND_APP_ID = text("""
    SELECT * FROM role WHERE name = :name AND app_id = :app_id
""")

INSERT_ROLE = text("""
    INSERT INTO role (app_id, name, description, created_at)
    VALUES (:app_id, :name, :description, :created_at)
""")

GET_ROLE_BY_ID = text("""
    SELECT * FROM role WHERE id = :role_id 
""")

# Membership Queries

GET_MEMBERSHIPS_BY_ROLE_ID = text("""
    SELECT id, role_id, app_id, user_id, created_at FROM membership WHERE role_id = :role_id ORDER BY created_at DESC
""")

INSERT_MEMBERSHIP = text("""
    INSERT INTO membership (user_id, app_id, role_id, created_at)
    VALUES (:user_id, :app_id, :role_id, :created_at)
""")

GET_MEMBERSHIP_BY_USER_ID_AND_ROLE_ID = text("""
    SELECT * FROM membership WHERE user_id = :user_id AND role_id = :role_id
""")

GET_MEMBERSHIPS_BY_USER_ID = text("""
    SELECT id, role_id, app_id, user_id, created_at FROM membership WHERE user_id = :user_id ORDER BY created_at DESC
""")
