import csv
from app.models import Pokemon
from app.database import engine
from sqlmodel import Session
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Annotated, Any, Literal

from pydantic import (
    AnyUrl,
    BeforeValidator,
    EmailStr,
    HttpUrl,
    PostgresDsn,
    computed_field,
    model_validator,
)
from pydantic_core import MultiHostUrl


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        # Env file in pokegame not backend
        env_file="../../.env",
        env_ignore_empty=True,
        extra="ignore",
    )
    # API_V1_STR: str = "/api/v1"
    SECRET_KEY: str
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    FRONTEND_HOST: str = "http://localhost:5173"
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"

    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyUrl] | str, BeforeValidator(parse_cors)
    ] = []

    @computed_field  # type: ignore[prop-decorator]
    @property
    def all_cors_origins(self) -> list[str]:
        return [str(origin).rstrip("/") for origin in self.BACKEND_CORS_ORIGINS] + [
            self.FRONTEND_HOST
        ]

    PROJECT_NAME: str
    SENTRY_DSN: HttpUrl | None = None
    POSTGRES_SERVER: str
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = ""

    @computed_field  # type: ignore[prop-decorator]
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme="postgresql+psycopg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )


def create_entry(pokemon: Pokemon) -> Pokemon:
    with Session(engine) as session:
        session.add(pokemon)
        session.commit()
        session.refresh(pokemon)
    return pokemon


def populate_db():
    with open("app/data/pokemon.csv", mode="r") as file:
        import_file = csv.reader(file)
        _header = next(import_file)
        for lines in import_file:
            ndex = int(lines[0][1:])
            name = lines[1]
            types = lines[2] + " " + lines[3] if len(lines) > 3 else lines[2]
            # print(f"ndex: {ndex}, name: {name}, types: '{types}'  ")
            create_entry(Pokemon(ndex=ndex, name=name, type=types))


settings = Settings()
if __name__ == "__main__":
    populate_db()
