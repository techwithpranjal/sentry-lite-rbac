from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Base settings class."""
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    APP_NAME: str = "Sentry Lite"
    DEBUG: bool = False
    TESTING: bool = False
    
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    DATABASE_URL: str = "sqlite:///db/sentry_lite.db"

    MAX_BCRYPT_BYTES: int = 72  # bcrypt limit

settings = Settings()

    