__all__ = ["settings"]

from functools import lru_cache
from pathlib import Path
from typing import Optional, Self
from pydantic import Field, PrivateAttr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from abc import ABC


BASE_DIR = Path(__file__).resolve().parent.parent
KEY_DIR = Path(__file__).resolve().parent / "key"


class AbstractSettings(BaseSettings, ABC):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env", env_file_encoding="utf-8", extra="ignore"
    )


class Auth(AbstractSettings):
    """
    Настройки для работы авторизационной системы.
    """

    access_token_time: int = Field(alias="ACCESS_TOKEN_TIME_SECONDS", default=600)
    refresh_token_time: int = Field(alias="REFRESH_TOKEN_TIME_SECONDS", default=3600)
    algoritm: str = Field(alias="AUTH_ALGORITM", default="RS256")

    # Приватные атрибуты для ключей
    _private_key: Optional[bytes] = PrivateAttr(default=None)
    _public_key: Optional[bytes] = PrivateAttr(default=None)

    @model_validator(mode="after")
    def load_keys_and_validate(self) -> Self:
        """Валидация + загрузка ключей в одном методе (Pydantic v2.4)"""
        # 1. Валидация логики токенов
        if self.access_token_time <= 0:
            raise ValueError("ACCESS_TOKEN_TIME_SECONDS должен быть > 0")
        if self.refresh_token_time <= self.access_token_time:
            raise ValueError(
                "REFRESH_TOKEN_TIME_SECONDS должен быть ДОЛЬШЕ access токена"
            )

        # 2. Загрузка ключей

        try:
            self._private_key = (KEY_DIR / "private_key.pem").read_bytes()
            self._public_key = (KEY_DIR / "public_key.pem").read_bytes()
        except FileNotFoundError as e:
            raise RuntimeError(
                f"Ключи не найдены: {e}. Убедитесь, что запустили generate_keys.sh"
            ) from None

        return self

    @property
    def PRIVATE_KEY(self) -> bytes:
        if self._private_key is None:
            raise RuntimeError("PRIVATE_KEY не загружен! Вызовите load_keys()")
        return self._private_key

    @property
    def PUBLIC_KEY(self) -> bytes:
        if self._public_key is None:
            raise RuntimeError("PUBLIC_KEY не загружен! Вызовите load_keys()")
        return self._public_key


class PostgresqlSettings(AbstractSettings):
    """
    Настройки для подключения к базе данных.
    Здесь есть параметры Optional с той целью, потому что может использоваться sqlite.
    """

    host: str | None = Field(alias="DATABASE_HOST", default=None)
    port: int | None = Field(alias="DATABASE_PORT_NETWORK", default=None)
    user: str | None = Field(alias="DATABASE_USER", default=None)
    password: str | None = Field(alias="DATABASE_PASSWORD", default=None)
    name: str = Field(alias="DATABASE_NAME")
    dialect: str = Field(alias="DATABASE_DIALECT")
    driver: str = Field(alias="DATABASE_DRIVER")

    @property
    def url(self) -> str:
        if self.dialect == "sqlite":
            return f"{self.dialect}+{self.driver}:///{self.name}"

        return f"{self.dialect}+{self.driver}://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class SQLAlchemySettings(AbstractSettings):
    "Настройки работы алхимии."

    # Параметры подключения
    echo: bool = True

    # Параметры поведения SQLAlchemy
    auto_flush: bool = True
    expire_on_commit: bool = False


class MinioSettings(AbstractSettings):
    """
    Настройки для подключения к MinIO.

    buckets_name захардкорен в bootstrap
    """

    endpoint: str = Field(alias="MINIO_ENDPOINT", default="localhost:9000")
    access_key: str = Field(alias="MINIO_ACCESS_KEY")
    secret_key: str = Field(alias="MINIO_SECRET_KEY")
    secure: bool = Field(alias="MINIO_SECURE", default=False)
    region: str | None = Field(alias="MINIO_REGION", default=None)
    jwt_secret: str = Field(alias="JWT_SECRET", default="my_super_secret_key_123")

    public_bucket: str | None = Field(alias="PUBLIC_BUCKET", default=None)
    private_bucket: str | None = Field(alias="PRIVATE_BUCKET", default=None)


class UserAdmin(AbstractSettings):
    mail: str = Field(alias="ADMIN_MAIL", default="admin@example.com")
    password: str = Field(alias="ADMIN_PASSWORD")


class Settings(AbstractSettings):
    db: PostgresqlSettings = PostgresqlSettings()
    alchemy: SQLAlchemySettings = SQLAlchemySettings()
    auth: Auth = Auth()
    minio: MinioSettings = MinioSettings()
    admin: UserAdmin = UserAdmin()


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings: Settings = get_settings()
