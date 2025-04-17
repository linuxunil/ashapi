from fastapi import APIRouter, Depends
from app.database import get_session
from sqlmodel import Session, select 
from app.models import Pokemon

router = APIRouter(
    tags=["pokemon"],
)



@router.get("/pokemon/")
async def get_pokedex(session: Session = Depends(get_session), limit: int = 300, offset: int = 0):
    pokemon = session.exec(select(Pokemon).limit(limit).offset(offset)).all()
    return pokemon

@router.get("/pokemon/{ndex}")
async def get_pokemon(ndex: int, session: Session = Depends(get_session)):
    pokemon = session.get(Pokemon, ndex)
    return pokemon
