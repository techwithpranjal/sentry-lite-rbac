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

