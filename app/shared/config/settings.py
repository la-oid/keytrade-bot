# Реализация настроек основана на статье:
# https://habr.com/ru/articles/866536/

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, SecretStr


class EnvBase(BaseSettings):
    """Базовый класс для всех env-настроек"""
    model_config = SettingsConfigDict(
        env_file = ".env",
        env_file_encoding = "utf-8",
        extra = "ignore"
    )


class TelegramSettings(EnvBase):
    """Настройки Telegram"""
    TOKEN: SecretStr = Field(..., description="Токен Telegram-бота")
    
    model_config = SettingsConfigDict(
        env_prefix = "TG_"
    )


class DatabaseSettings(EnvBase):
    """Настройки базы данных"""
    URL: str = Field(..., description="Строка подключения к базе данных")
    
    model_config = SettingsConfigDict(
        env_prefix = "DB_"
    )


class Settings(BaseSettings):
    """Центральный класс для всех настроек"""
    telegram: TelegramSettings = Field(default_factory=TelegramSettings)
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    
    @classmethod
    def load(cls) -> "Settings":
        return cls()


settings = Settings.load()
