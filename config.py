from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    anthropic_api_key: str
    host: str = "0.0.0.0"
    port: int = 8000
    env: str = "development"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
