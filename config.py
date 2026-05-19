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


 
class Settings:
    anthropic_api_key: str = os.environ.get("ANTHROPIC_API_KEY", "")
    host: str = os.environ.get("HOST", "0.0.0.0")
    port: int = int(os.environ.get("PORT", "8000"))
    env: str = os.environ.get("ENV", "production")
 
settings = Settings()