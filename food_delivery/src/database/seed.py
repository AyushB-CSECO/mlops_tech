import pandas as pd
import os, sys
from pathlib import Path

from database import SessionLocal, create_tables
from models import Country, City, City_Statistics, Cuisine
from models import Delivery_Metrics, Restaurant, Menu
from models import Price_History, Restaurant_Features
from models import Nutrition, Restaurant_Statistics

# Reset to Base Folder
FILE_PATH = Path(__file__).resolve()
BASE_PATH = FILE_PATH.parent.parent.parent

if str(BASE_PATH) not in sys.path:
    sys.path.insert(0, str(BASE_PATH))
os.chdir(BASE_PATH)

from src.data.validation import colnames_lowercase


def load_records(fname: str, data_model) -> list:
    f_path = BASE_PATH / "data" / "raw" / fname
    df = pd.read_csv(f_path)
    df = colnames_lowercase(df)
    records = df.to_dict(orient="records")
    return [data_model(**record) for record in records]


country_records = load_records('countries.csv', Country)
city_records = load_records('cities.csv', City)
city_statistics_records = load_records('city_statistics.csv'
                                       ,City_Statistics)
cuisine_records = load_records('cuisines.csv', Cuisine)
delivery_metrics_records = load_records('delivery_metrics.csv'
                                        , Delivery_Metrics)
restaurant_records = load_records('restaurants.csv', Restaurant)
menu_records = load_records('menus.csv', Menu)
nutrition_records = load_records('nutrition.csv', Nutrition)
price_history_records = load_records('price_history.csv'
                                        , Price_History)
restaurant_feature_records = load_records('restaurant_features.csv'
                                            , Restaurant_Features)
restaurant_statistics_records = load_records(
                                    'restaurant_statistics.csv'
                                    , Restaurant_Statistics)

def seed_database():
    # Create model tables in DB
    create_tables()

    # Initiate DB session for data transactions
    db = SessionLocal()

    try:
        records_list = [country_records, city_records, city_statistics_records
                ,cuisine_records, delivery_metrics_records, restaurant_records
                ,menu_records, nutrition_records, price_history_records
                ,restaurant_feature_records, restaurant_statistics_records]
        
        for records in records_list:
            db.add_all(records)
            db.commit()

    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()