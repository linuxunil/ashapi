from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.database import create_db_and_tables
from app.routers import router
from app.scripts import populate_db
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)
app.mount("/sprite", StaticFiles(directory="/code/app/static"), name="static")
app.include_router(router)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    populate_db()
