from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Apartment Sales API"
    database_url: str = "sqlite:///./apartments.db"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
