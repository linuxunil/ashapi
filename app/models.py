from sqlmodel import SQLModel, Field


class Pokemon(SQLModel, table=True):
    ndex: int = Field(primary_key=True)
    name: str
    type: str


class HighScore(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user: str
    score: int
