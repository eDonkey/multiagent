from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    APP_ENV: str = "development"
    APP_DEBUG: bool = True

    WEBHOOK_SECRET: str

    ANTHROPIC_API_KEY: str | None = None
    KAPSO_API_KEY: str
    KAPSO_DB_URL: str
    KAPSO_PHONE_NUMBER_ID: str

    PHONE_RENA: str
    PHONE_FRAN: str | None = None
    PHONE_NEGOCIO: str | None = None

    TEAM_EMAIL_RENA: str = "renatopiermarinih@gmail.com"
    TEAM_EMAIL_FRAN: str | None = None

    SERPER_API_KEY: str | None = None
    GMAIL_TOKEN_PATH: str | None = None

    MAX_THREADS: int = 4
    AGENT_TIMEOUT_SECONDS: int = 120
    GLOBAL_RATE_LIMIT: str = "60/minute"
    PHONE_RATE_LIMIT: str = "10/minute"
    CONVERSATION_WINDOW: int = 20
    CONVERSATION_TIMEOUT_MINUTES: int = 30


settings = Settings()
