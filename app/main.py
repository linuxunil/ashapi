from fastapi import FastAPI
from app.models import Pokemon
from app.database import create_db_and_tables
from app.routers import router
from app.scripts import populate_db

app = FastAPI()
app.include_router(router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    populate_db()
