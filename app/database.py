from typing import Annotated
from fastapi import Depends
from sqlmodel import SQLModel, Session, create_engine

sql_file_name = "pokedex.db"
sqlite_url = f"sqlite:///{sql_file_name}"

connection_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connection_args)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
