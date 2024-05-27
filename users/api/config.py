from pydantic_settings import BaseSettings
from pydantic import BaseModel


class AppConfig(BaseModel):
    host: str
    port: int
    reload: bool


class DBConfig(BaseModel):
    host: str
    port: int
    user: str
    password: str
    name: str


class Config(BaseSettings):
    class Config:
        env_nested_delimiter = "__"

    app: AppConfig
    db: DBConfig

    secret_key: str
    hash_algorithm: str

    @property
    def db_url(self) -> str:
        return f"postgresql+asyncpg://{self.db.user}:{self.db.password}@{self.db.host}:{self.db.port}/{self.db.name}"


config = Config()
