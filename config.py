# from pydantic_settings import BaseSettings

# class Settings(BaseSettings):
#     anthropic_api_key: str
#     host: str = "0.0.0.0"
#     port: int = 8000
#     env: str = "development"

#     class Config:
#         env_file = ".env"
#         extra = "ignore"

# settings = Settings()
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8080"))
    env: str = os.getenv("ENV", "production")

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()