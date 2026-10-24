from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
class Settings(BaseSettings):
    DATABASE_URL: SecretStr
    BOT_TOKEN: SecretStr
    model_config = SettingsConfigDict(env_file=BASE_DIR /".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()