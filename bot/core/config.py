from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Конфигурация приложения из окружения (.env)."""
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    bot_token: str
    db_url: str | None = None
    redis_url: str
    use_webhook: bool = False
    admin_ids: list[int] = []
    log_level: str = "INFO"
    rate_limit_limit: int = 5
    rate_limit_period: float = 1.0
    rate_limit_notify: bool = True
    command_rate_limit_limit: int = 3
    command_rate_limit_period: float = 5.0

    @field_validator("admin_ids", mode="before")
    @classmethod
    def _parse_admin_ids(cls, value: str | list[int] | None) -> list[int]:
        if value is None or value == "":
            return []
        if isinstance(value, list):
            return [int(item) for item in value]
        return [int(item.strip()) for item in str(value).split(",") if item.strip()]

settings = Settings()
