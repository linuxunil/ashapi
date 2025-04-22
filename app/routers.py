from fastapi import APIRouter, Depends
from app.database import get_session
from sqlmodel import Session, select
from app.models import Pokemon, HighScore

pokemon_router = APIRouter(tags=["pokemon"], prefix="pokemon")

score_router = APIRouter(
    tags=["score"],
    prefix="score",
)


@score_router.get("/{user}")
async def get_user_score(user: str, session: Session = Depends(get_session)):
    score = session.get(HighScore, user)
    return score


@score_router.post("/new}")
async def set_user_score(score: HighScore, session: Session = Depends(get_session)):
    session.add(score)
    session.commit()
    session.refresh(score)
    return score


@pokemon_router.get("/")
async def get_pokedex(
    session: Session = Depends(get_session), limit: int = 300, offset: int = 0
):
    pokemon = session.exec(select(Pokemon).limit(limit).offset(offset)).all()
    return pokemon


@pokemon_router.get("/{ndex}")
async def get_pokemon(ndex: int, session: Session = Depends(get_session)):
    pokemon = session.get(Pokemon, ndex)
    return pokemon
