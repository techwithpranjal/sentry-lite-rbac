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
    SELECT id, name, slug, description, poc_user_email, created_at FROM app ORDER BY created_at DESC
""")

GET_APP_BY_APP_ID = text("""
    SELECT * FROM app WHERE id = :app_id
""")

GET_APP_BY_SLUG = text("""
    SELECT * FROM app WHERE slug = :slug
""")

INSERT_APP = text("""
    INSERT INTO app (name, slug, description, poc_user_email, created_at)
    VALUES (:name, :slug, :description, :poc_user_email, :created_at)
""")

GET_OWNED_APPS_BY_USER_EMAIL = text("""
    SELECT id, name, slug, description, poc_user_email, created_at FROM app WHERE poc_user_email = :email ORDER BY created_at DESC
""")

CHECK_IF_USER_IS_APP_OWNER = text("""
    SELECT 1 FROM app WHERE id = :app_id AND poc_user_email = :poc_user_email
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
    SELECT
        m.id,
        m.role_id,
        r.name AS role_name,
        m.app_id,
        a.name AS app_name,
        m.user_email,
        m.created_at,
        m.created_by
    FROM membership m
    JOIN app a ON a.id = m.app_id
    JOIN role r ON r.id = m.role_id
    WHERE m.role_id = :role_id
    ORDER BY m.created_at DESC
""")

INSERT_MEMBERSHIP = text("""
    INSERT INTO membership (user_email, app_id, role_id, created_at, created_by)
    VALUES (:user_email, :app_id, :role_id, :created_at, :created_by)
""")

GET_MEMBERSHIP_BY_USER_EMAIL_AND_ROLE_ID = text("""
    SELECT
        m.id,
        m.user_email,
        m.role_id,
        r.name AS role_name,
        m.app_id,
        a.name AS app_name,
        m.created_at,
        m.created_by
    FROM membership m
    JOIN role r ON r.id = m.role_id
    JOIN app a ON a.id = m.app_id
    WHERE m.user_email = :user_email
      AND m.role_id = :role_id
""")

GET_MEMBERSHIP_BY_ID = text("""
    SELECT * FROM membership WHERE id = :id
""")

GET_MEMBERSHIPS_BY_USER_EMAIL = text("""
    SELECT
        m.id,
        m.user_email,
        m.app_id,
        a.name AS app_name,
        m.role_id,
        r.name AS role_name,
        m.created_at,
        m.created_by
    FROM membership m
    JOIN app a ON a.id = m.app_id
    JOIN role r ON r.id = m.role_id
    WHERE m.user_email = :user_email
    ORDER BY m.created_at DESC
""")

DELETE_MEMBERSHIP_BY_ID = text("""
    DELETE FROM membership WHERE id = :id
""")

# Request Queries

GET_REQUEST_BY_USER_EMAIL_AND_ROLE_ID = text("""
    SELECT
        r.id,
        r.user_email,
        r.app_id,
        a.name AS app_name,
        r.role_id,
        ro.name AS role_name,
        r.justification,
        r.status,
        r.created_at,
        r.updated_at,
        r.updated_by
    FROM request r
    JOIN app a ON a.id = r.app_id
    JOIN role ro ON ro.id = r.role_id
    WHERE r.user_email = :email
      AND r.role_id = :role_id
""")

INSERT_REQUEST = text("""
    INSERT INTO request (user_email, app_id, role_id, justification, status, created_at)
    VALUES (:user_email, :app_id, :role_id, :justification, 'pending', :created_at)
""")

GET_REQUESTS_BY_USER_EMAIL = text("""
    SELECT
        r.id,
        r.user_email,
        r.app_id,
        a.name AS app_name,
        r.role_id,
        ro.name AS role_name,
        r.justification,
        r.status,
        r.created_at,
        r.updated_by,
        r.updated_at
    FROM request r
    JOIN app a ON a.id = r.app_id
    JOIN role ro ON ro.id = r.role_id
    WHERE r.user_email = :email
    ORDER BY r.created_at DESC
""")

GET_REQUESTS_BY_REQUEST_ID = text("""
    SELECT
        r.id,
        r.user_email,
        r.app_id,
        a.name AS app_name,
        r.role_id,
        ro.name AS role_name,
        r.justification,
        r.status,
        r.created_at,
        r.updated_by,
        r.updated_at
    FROM request r
    JOIN app a ON a.id = r.app_id
    JOIN role ro ON ro.id = r.role_id
    WHERE r.id = :request_id
""")

GET_REQUESTS_BY_POC = text("""
    SELECT
        r.id,
        r.user_email,
        r.app_id,
        a.name AS app_name,
        r.role_id,
        ro.name AS role_name,
        r.justification,
        r.status,
        r.created_at,
        r.updated_by,
        r.updated_at
    FROM request r
    JOIN app a ON r.app_id = a.id
    JOIN role ro ON r.role_id = ro.id
    WHERE a.poc_user_email = :poc_user_email
    ORDER BY r.created_at DESC
""")

UPDATE_REQUEST_STATUS = text("""
    UPDATE request SET status = :status, updated_by = :updated_by, updated_at = :updated_at
    WHERE id = :request_id
""")


# Admin Queries

ADMIN_OVERVIEW = text("""
SELECT
  (SELECT COUNT(*) FROM user) AS users,
  (SELECT COUNT(*) FROM app) AS applications,
  (SELECT COUNT(*) FROM role) AS roles,
  (SELECT COUNT(*) FROM membership) AS memberships,
  (SELECT COUNT(*) FROM request WHERE status = 'pending') AS pending_requests,

  (SELECT COUNT(*) FROM app WHERE poc_user_email IS NULL) AS apps_without_owner,

  (SELECT COUNT(*) FROM role r
     LEFT JOIN membership m ON r.id = m.role_id
     WHERE m.id IS NULL) AS roles_without_members,

  (SELECT CAST(
      JULIANDAY('now') - JULIANDAY(MIN(created_at))
    AS INT)
    FROM request
    WHERE status = 'pending'
  ) AS oldest_pending_request_days,

  -- Activity Snapshot
  (SELECT COUNT(*) FROM request
     WHERE created_at >= DATETIME('now', '-1 day')
  ) AS requests_last_24h,

  (SELECT COUNT(*) FROM request
     WHERE status = 'approved'
       AND updated_at >= DATETIME('now', '-1 day')
  ) AS approvals_last_24h,

  (SELECT COUNT(*) FROM membership
     WHERE created_at >= DATETIME('now', '-1 day')
  ) AS memberships_last_24h,

  (SELECT COUNT(*) FROM app
     WHERE created_at >= DATETIME('now', '-7 day')
  ) AS apps_last_7d
""")

GET_PENDING_REQUESTS = text("""
    SELECT
    r.id,
    r.user_email,
    a.name AS app_name,
    ro.name AS role_name,
    r.status,
    r.created_at
    FROM request r
    JOIN app a ON r.app_id = a.id
    JOIN role ro ON r.role_id = ro.id
    WHERE r.status = 'pending'
    ORDER BY r.created_at DESC
    LIMIT 10;
""")

ADMIN_APPS = text("""
SELECT id, name, slug, description, poc_user_email, created_at
FROM app
ORDER BY created_at DESC;
""")

ADMIN_ROLES = text("""
SELECT
  r.id            AS role_id,
  r.name          AS role_name,
  a.name          AS app_name,
  a.slug          AS app_slug,
  COUNT(m.id)     AS members_count,
  r.created_at    AS created_at
FROM role r
JOIN app a ON r.app_id = a.id
LEFT JOIN membership m ON r.id = m.role_id
GROUP BY r.id, a.name, a.slug
ORDER BY r.created_at DESC;
""")

ADMIN_REQUESTS = text("""
SELECT
  r.id            AS request_id,
  r.user_email    AS user_email,

  a.name          AS app_name,
  ro.name         AS role_name,

  r.status        AS status,
  r.justification AS justification,

  r.created_at    AS created_at,
  r.updated_by    AS updated_by,
  r.updated_at    AS updated_at
FROM request r
JOIN app a  ON r.app_id = a.id
JOIN role ro ON r.role_id = ro.id
ORDER BY r.created_at DESC;
""")

ADMIN_MEMBERSHIPS = text("""
SELECT
  m.id            AS id,
  m.user_email    AS user_email,
  m.app_id        AS app_id,
  a.name          AS app_name,
  m.role_id       AS role_id,
  r.name          AS role_name,
  m.created_at    AS created_at,
  m.created_by    AS created_by
FROM membership m
JOIN app a  ON m.app_id = a.id
JOIN role r ON m.role_id = r.id
ORDER BY m.created_at DESC;
""")

# Additional Queries

TRUNCATE_REQUEST_TABLE = text("""
    DELETE FROM request
""")

TRUNCATE_MEMBERSHIP_TABLE = text("""
    DELETE FROM membership
""")

TRUNCATE_ROLE_TABLE = text("""
    DELETE FROM role
""")

TRUNCATE_APP_TABLE = text("""
    DELETE FROM app
""")

TRUNCATE_USER_TABLE = text("""
    DELETE FROM user
""")
