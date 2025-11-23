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

GET_APP_BY_SLUG = text("""
    SELECT * FROM app WHERE slug = :slug
""")

INSERT_APP = text("""
    INSERT INTO app (name, slug, description, poc_user_id, created_at)
    VALUES (:name, :slug, :description, :poc_user_id, :created_at)
""")