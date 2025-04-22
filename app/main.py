from typing import Annotated

from fastapi import APIRouter, Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlmodel import Field, Session, SQLModel, create_engine, select

import app.settings
from app.scripts import populate_db

settings = app.settings.Settings()
engine = create_engine(str(settings.SQL_ALCHEMY_DATABASE_URI))

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/sprite", StaticFiles(directory="/code/app/static"), name="static")


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    populate_db(get_session())


# Database


class Pokemon(SQLModel, table=True):
    ndex: int = Field(primary_key=True)
    name: str
    type: str


class HighScore(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user: str
    score: int


## database


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


pokemon_router = APIRouter(tags=["pokemon"], prefix="pokemon")

score_router = APIRouter(
    tags=["score"],
    prefix="score",
)


# Routes
@app.get("/score/{user}")
async def get_user_score(user: str, session: Session = Depends(get_session)):
    score = session.get(HighScore, user)
    return score


@app.post("/score/new}")
async def set_user_score(score: HighScore, session: Session = Depends(get_session)):
    session.add(score)
    session.commit()
    session.refresh(score)
    return score


@app.get("/pokemon/")
async def get_pokedex(
    session: Session = Depends(get_session), limit: int = 300, offset: int = 0
):
    pokemon = session.exec(select(Pokemon).limit(limit).offset(offset)).all()
    return pokemon


@app.get("/pokemon/{ndex}")
async def get_pokemon(ndex: int, session: Session = Depends(get_session)):
    pokemon = session.get(Pokemon, ndex)
    return pokemon
