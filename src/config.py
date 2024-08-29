from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent


class DbSettings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    @property
    def database_url_asyncpg(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


class JwtSettings(BaseSettings):
    private_key_path: Path = BASE_DIR / "certs" / "private_key.pem"
    public_key_path: Path = BASE_DIR / "certs" / "public_key.pem"

    ALGORITHM: str
    ACCESS_TOKEN_NAME: str
    REFRESH_TOKEN_NAME: str
    ACCESS_TOKEN_EXPIRE_TIME: int
    REFRESH_TOKEN_EXPIRE_TIME: int

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')


class Settings(BaseSettings):
    db: DbSettings = DbSettings()
    jwt: JwtSettings = JwtSettings()


settings = Settings()
