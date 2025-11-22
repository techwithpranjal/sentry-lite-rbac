from sqlalchemy import text

GET_USER_BY_EMAIL = text("""
    SELECT * FROM users WHERE email = :email
""")