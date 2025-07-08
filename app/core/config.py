import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    db_user: str = os.getenv("DB_USER", "postgres")
    db_password: str = os.getenv("DB_PASSWORD", "password")
    db_host: str = os.getenv("DB_HOST", "pgbouncer")
    db_port: str = os.getenv("DB_PORT", "6432")
    db_name: str = os.getenv("DB_NAME", "postgres")

    database_url: str = (
        f"postgresql+psycopg2://{db_user}:{db_password}@"
        f"{db_host}:{db_port}/{db_name}"
    )

    secret_key: str = os.getenv("SECRET_KEY")
    access_token_ttl: str = os.getenv("ACCESS_TOKEN_TTL")

    class Config:
        env_file = ".env"

settings = Settings()