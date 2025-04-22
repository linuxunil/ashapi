import csv

from sqlmodel import Session

from app.models import Pokemon


def create_entry(pokemon: Pokemon, session: Session) -> Pokemon:
    session.add(pokemon)
    session.commit()
    session.refresh(pokemon)
    return pokemon


def populate_db(session: Session):
    with open("app/data/pokemon.csv", mode="r") as file:
        import_file = csv.reader(file)
        _header = next(import_file)
        for lines in import_file:
            ndex = int(lines[0][1:])
            name = lines[1]
            types = lines[2] + " " + lines[3] if len(lines) > 3 else lines[2]
            # print(f"ndex: {ndex}, name: {name}, types: '{types}'  ")
            create_entry(Pokemon(ndex=ndex, name=name, type=types), session)
