import pandas as pd
import os, sys
from pathlib import Path

from database import SessionLocal, create_tables
from models import Country

# Reset to Base Folder
FILE_PATH = Path(__file__).resolve()
BASE_PATH = FILE_PATH.parent.parent.parent

if str(BASE_PATH) not in sys.path:
    sys.path.insert(0, str(BASE_PATH))
os.chdir(BASE_PATH)

from src.data.validation import colnames_lowercase

f_path = BASE_PATH / "data" / "raw" / "countries.csv"

def load_country():
    df = pd.read_csv(f_path)
    df = colnames_lowercase(df)
    records = df.to_dict(orient="records")

    return [Country(**record) for record in records]

def seed_database():
    # Create model tables in DB
    create_tables()

    # Initiate DB session for data transactions
    db = SessionLocal()

    try:
        country_records = load_country()
        db.add_all(country_records)

        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()