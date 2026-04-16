from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    APP_NAME: str = 'dealer-agents-mvp'
    APP_ENV: str = 'development'
    APP_DEBUG: bool = True
    PORT: int = 8000

    DATABASE_URL: str
    REDIS_URL: str
    SECRET_KEY: str

    OPENAI_API_KEY: str = ''
    DEFAULT_LLM_MODEL: str = 'gpt-4.1-mini'

    WHATSAPP_VERIFY_TOKEN: str
    WHATSAPP_ACCESS_TOKEN: str
    WHATSAPP_PHONE_NUMBER_ID: str

    DEFAULT_TIMEZONE: str = 'America/Argentina/Buenos_Aires'
    LOG_LEVEL: str = 'INFO'


settings = Settings()
