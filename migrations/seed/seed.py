import pathlib
import sys

abspath = str(pathlib.Path(__file__).parent.parent.parent.absolute())  # noqa: E402
sys.path.insert(0, abspath)  # noqa: E402

from hotel_reservation.database import session_factory
from sqlalchemyseed import load_entities_from_json
from sqlalchemyseed import Seeder


def run():
    try:
        session = session_factory()
        entities = load_entities_from_json("migrations/seed/data.json")
        seeder = Seeder(session)
        seeder.seed(entities)
        session.commit()
    except Exception as seed_exception:
        print(f"Error during seed ingestion process: {seed_exception}")


if __name__ == "__main__":
    run()
