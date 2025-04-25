from pydantic_settings import BaseSettings, SettingsConfigDict


class ApiSettings(BaseSettings):
    DB_HOST: str = ""
    DB_PORT: int = 5431
    DB_USER: str = ""
    DB_PASSWORD: str = ""
    DB_NAME: str = ""
    DB_SCHEMA: str = ""
    DB_POOL_TIMEOUT: int = 30  # Tiempo máximo de espera
    DB_CONNECT_TIMEOUT: int = 5  # Tiempo máximo para establecer conexión
    DB_COMMAND_TIMEOUT: int = 10  # segundos
    DB_POOL_SIZE: int = 20
    Empty_BASE_URL: str = 'https://rickandmortyapi.com/'

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

    @property
    def DATABASE_URL(self):
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


settings = ApiSettings()
