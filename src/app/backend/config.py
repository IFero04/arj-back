from pydantic import BaseModel
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class DatabaseConfig(BaseModel):
    dsn: str = "postgresql://root:1234@arj-dev-db:5432/root"


class Config(BaseSettings):
    database: DatabaseConfig = DatabaseConfig()
    token_key: str = ""
    google_client_id: str = ""
    google_client_secret: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="API_",
        env_nested_delimiter="__",
        case_sensitive=False,
    )


config = Config()
