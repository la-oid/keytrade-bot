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
    BUYER_TOKEN: SecretStr = Field(..., description="Токен правого бота (скупщик)")
    SELLER_TOKEN: SecretStr = Field(..., description="Токен левого бота (продажник)")
    ADMIN_TOKEN: SecretStr = Field(..., description="Токен админ-бота (контролер)")
    ADMIN_IDS: list[int] = Field(default_factory=list, description="Список Telegram ID админов")

    model_config = SettingsConfigDict(
        env_prefix="TG_"
    )


class AppSettings(EnvBase):
    """Настройки приложения"""
    PAYMENT_URL: str = Field(..., description="Базовый URL страницы оплаты")
    
    model_config = SettingsConfigDict(
        env_prefix="APP_"
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
    app: AppSettings = Field(default_factory=AppSettings)
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    
    @classmethod
    def load(cls) -> "Settings":
        return cls()


settings = Settings.load()