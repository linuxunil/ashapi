from sqlmodel import SQLModel, Field


class Pokemon(SQLModel, table=True):
    ndex: int = Field(primary_key=True)
    name: str
    type: str
