import pandas as pd
import os, sys
from pathlib import Path

from database import SessionLocal, create_tables
from models import Country, City

# Reset to Base Folder
FILE_PATH = Path(__file__).resolve()
BASE_PATH = FILE_PATH.parent.parent.parent

if str(BASE_PATH) not in sys.path:
    sys.path.insert(0, str(BASE_PATH))
os.chdir(BASE_PATH)

from src.data.validation import colnames_lowercase


def get_records(fname: str) -> list:
    f_path = BASE_PATH / "data" / "raw" / fname
    df = pd.read_csv(f_path)
    df = colnames_lowercase(df)
    records = df.to_dict(orient="records")
    return records


def load_country():
    records = get_records('countries.csv')
    return [Country(**record) for record in records]

def load_city(): 
    records = get_records('cities.csv')
    return [City(**record) for record in records]


def seed_database():
    # Create model tables in DB
    create_tables()

    # Initiate DB session for data transactions
    db = SessionLocal()

    try:
        country_records = load_country()
        db.add_all(country_records)
        db.commit()

        city_records = load_city()
        db.add_all(city_records)
        db.commit()

    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()