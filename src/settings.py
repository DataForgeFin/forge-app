from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    mongo_uri: str = "mongodb://localhost:27017"
    mongo_db: str = "forge_sync"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
