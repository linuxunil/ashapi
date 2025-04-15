import csv
from app.models import Pokemon
from app.database import engine 
from sqlmodel import Session


def create_entry(pokemon: Pokemon) -> Pokemon:
    with Session(engine) as session:
        session.add(pokemon)
        session.commit()
        session.refresh(pokemon)
    return pokemon

if __name__ == "__main__":
    populate_db()

def populate_db():
    with open("app/data/pokemon.csv", mode="r") as file:
        import_file = csv.reader(file)
        header = next(import_file)
        for lines in import_file:
            ndex = int(lines[0][1:])
            name = lines[1]
            types = lines[2] + " " + lines[3] if len(lines) > 3 else lines[2]
            #print(f"ndex: {ndex}, name: {name}, types: '{types}'  ")
            create_entry(Pokemon(ndex=ndex, name=name, type=types)) 

