from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "sqlite:///./pumphouseup.db"
    secret_key: str = "set-secret-key-in-environment"
    access_token_expire_minutes: int = 480
    upload_dir: str = "storage/uploads"
    api_url: str = "http://localhost:8000"
    admin_email: str = "admin@pumphouseup.local"
    admin_password: str = "set-admin-password-in-environment"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
