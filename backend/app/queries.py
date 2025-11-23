from sqlalchemy import text

GET_USER_BY_EMAIL = text("""
    SELECT * FROM users WHERE email = :email
""")

INSERT_USER = text("""
    INSERT INTO users (email, password_hash) VALUES (:email, :password_hash)
""")