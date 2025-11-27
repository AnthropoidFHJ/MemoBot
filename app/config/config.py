try:
    from pydantic_settings import BaseSettings
except ImportError:
    from pydantic import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Personal AI Assistant"
    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "openai/gpt-oss-120b"
    HISTORY_FILE: str = "history.json"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()