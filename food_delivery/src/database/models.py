from sqlalchemy import String, Integer, Float
from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy import ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pathlib import Path

from database import Base


class Country(Base):
    __tablename__ = "country"
    # Columns Schema
    country: Mapped[str] =  mapped_column(String, primary_key=True)
    region: Mapped[str | None] = mapped_column(String)
    income_group: Mapped[str | None] = mapped_column(String)
    currency: Mapped[str] = mapped_column(String, unique=True)
    timezone: Mapped[str | None] = mapped_column(String) 
    iso_code: Mapped[str | None] = mapped_column(String, unique=True)

class City(Base):
    __tablename__ = "city"
    # Columns Schema
    city: Mapped[str] = mapped_column(String)
    country: Mapped[str] = mapped_column(String, ForeignKey("country.country"))
    population: Mapped[int | None] = mapped_column(Integer)
    area_km2: Mapped[float | None] = mapped_column(Float)
    urban_density: Mapped[int | None] = mapped_column(Integer)
    tourism_index: Mapped[float] = mapped_column(Float)
    average_income: Mapped[int] = mapped_column(Integer)
    cost_of_living_index: Mapped[int] = mapped_column(Integer)
    weather_zone: Mapped[str | None] = mapped_column(String) 

    __table_args__ = (
        PrimaryKeyConstraint('city', 'country'),
    )

class City_Statistics(Base):
    __tablename__ = "city_statistics"
    # Columns Schema
    city: Mapped[str] = mapped_column(String)
    country: Mapped[str] = mapped_column(String)
    restaurant_density: Mapped[float | None] = mapped_column(Float)
    cuisine_diversity_index: Mapped[float | None] = mapped_column(Float)
    average_rating: Mapped[float] = mapped_column(Float)
    average_menu_price: Mapped[float | None] = mapped_column(Float)
    delivery_coverage: Mapped[float] = mapped_column(Float)

    __table_args__ = (
        PrimaryKeyConstraint('city', 'country'),
        ForeignKeyConstraint(
            ['city', 'country'],
            ['city.city', 'city.country']
        )
    )

class Cuisine(Base):
    __tablename__ = "cuisine"
    # Columns Schema
    cuisine_id: Mapped[str] = mapped_column(String, primary_key=True)
    cuisine_name: Mapped[str] = mapped_column(String, unique=True)
    parent_cuisine: Mapped[str | None] = mapped_column(String)
    region: Mapped[str] = mapped_column(String, ForeignKey('country.region'))
    




if __name__ == "__main__":
    print("All libraries imported successfully.")
