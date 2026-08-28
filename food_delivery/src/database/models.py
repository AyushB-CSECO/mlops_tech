from sqlalchemy import String, Integer, Float, Boolean, DateTime
from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy import ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from pathlib import Path

from database import Base

class Country(Base):
    __tablename__ = "country"

    country: Mapped[str] =  mapped_column(String, primary_key=True)
    region: Mapped[str | None] = mapped_column(String)
    income_group: Mapped[str | None] = mapped_column(String)
    currency: Mapped[str] = mapped_column(String, unique=True)
    timezone: Mapped[str | None] = mapped_column(String) 
    iso_code: Mapped[str | None] = mapped_column(String, unique=True)

class City(Base):
    __tablename__ = "city"

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

    cuisine_id: Mapped[str] = mapped_column(String, primary_key=True)
    cuisine_name: Mapped[str] = mapped_column(String, unique=True)
    parent_cuisine: Mapped[str | None] = mapped_column(String)
    region: Mapped[str] = mapped_column(String, ForeignKey('country.region'))

class Delivery_Metrics(Base):
    __tablename__ = "delivery_metrics"

    restaurant_id: Mapped[str] = mapped_column(String, primary_key=True)
    delivery_fee: Mapped[float] = mapped_column(Float)
    service_fee: Mapped[float | None] = mapped_column(Float)
    packaging_fee: Mapped[float | None] = mapped_column(Float)
    estimated_delivery_time: Mapped[int | None] = mapped_column(Integer)
    average_delivery_time: Mapped[int] = mapped_column(Integer)
    peak_hour_multiplier: Mapped[float | None] = mapped_column(Float)
    minimum_order: Mapped[float | None] = mapped_column(Float)
    cancellation_rate: Mapped[float | None] = mapped_column(Float)
    availability: Mapped[bool | None] = mapped_column(Boolean)

class Restaurant(Base):
    __tablename__ = "restaurant"

    restaurant_id: Mapped[str] = mapped_column(String, primary_key=True)
    restaurant_name: Mapped[str] = mapped_column(String, unique=True)
    chain_local: Mapped[str | None] = mapped_column(String)
    cuisine: Mapped[str] = mapped_column(String, ForeignKey("cuisine.cuisine_name"))
    latitude: Mapped[float] = mapped_column(Float) 
    longitude: Mapped[float] = mapped_column(Float)
    city: Mapped[str] = mapped_column(String, ForeignKey("city.city"))
    country: Mapped[str] = mapped_column(String, ForeignKey("country.country"))
    opening_year: Mapped[int | None] = mapped_column(Integer) 
    delivery_available: Mapped[bool] = mapped_column(Boolean)
    takeaway: Mapped[bool] = mapped_column(Boolean)
    dine_in: Mapped[bool | None] = mapped_column(Boolean)
    reservations: Mapped[bool | None] = mapped_column(Boolean)
    price_level: Mapped[int | None] = mapped_column(Integer)
    average_rating: Mapped[float | None] = mapped_column(Float)
    review_count: Mapped[int | None] = mapped_column(Integer)
    business_status: Mapped[str] = mapped_column(String)

class Menu(Base):
    __tablename__ = "menu"

    menu_id: Mapped[str] = mapped_column(String)
    restaurant_id: Mapped[str] = mapped_column(String, ForeignKey("restaurant.restaurant_id"))
    food_category: Mapped[str | None] = mapped_column(String)
    item_name: Mapped[str] = mapped_column(String)
    price: Mapped[float | None] = mapped_column(Float)
    currency: Mapped[str] = mapped_column(String, ForeignKey("country.currency"))
    calories: Mapped[int | None] = mapped_column(Integer)
    protein: Mapped[float | None] = mapped_column(Float)
    fat: Mapped[float | None] = mapped_column(Float) 
    carbohydrates: Mapped[float | None] = mapped_column(Float)
    sugar: Mapped[float | None] = mapped_column(Float)
    sodium: Mapped[float | None] = mapped_column(Float) 
    vegetarian: Mapped[bool | None] = mapped_column(Boolean)
    vegan: Mapped[bool | None] = mapped_column(Boolean)
    gluten_free: Mapped[bool | None] = mapped_column(Boolean)

    __table_args__ = (
        PrimaryKeyConstraint('menu_id', 'item_name'),
    )

class Nutrition(Base):
    __tablename__ = "nutrition"

    menu_id: Mapped[str] = mapped_column(String)
    item_name: Mapped[str] = mapped_column(String)
    calories: Mapped[int | None] = mapped_column(Integer)
    protein: Mapped[float | None] = mapped_column(Float)
    fat: Mapped[float | None] = mapped_column(Float) 
    carbohydrates: Mapped[float | None] = mapped_column(Float)
    sugar: Mapped[float | None] = mapped_column(Float)
    sodium: Mapped[float | None] = mapped_column(Float) 
    vegetarian: Mapped[bool | None] = mapped_column(Boolean)
    vegan: Mapped[bool | None] = mapped_column(Boolean)
    gluten_free: Mapped[bool | None] = mapped_column(Boolean)

    __table_args__ = (
        PrimaryKeyConstraint('menu_id', 'item_name'),
        ForeignKeyConstraint(
            ['menu_id', 'item_name'],
            ['menu.menu_id', 'menu.item_name']
        )
    )
    
class Price_History(Base):
    __tablename__ = "price_history"

    menu_id: Mapped[str] = mapped_column(String, ForeignKey("menu.menu_id")
                                , primary_key=True)
    timestamp: Mapped[str] = mapped_column(String)
    current_price: Mapped[float] = mapped_column(Float)
    previous_price: Mapped[float] = mapped_column(Float)
    price_change: Mapped[float] = mapped_column(Float)

class Restaurant_Features(Base):
    __tablename__ = "restaurant_features"

    restaurant_id: Mapped[str] = mapped_column(String, 
                                    ForeignKey("restaurant.restaurant_id"),
                                    primary_key=True) 
    outdoor_seating: Mapped[bool | None] = mapped_column(Boolean)
    wifi: Mapped[bool | None] = mapped_column(Boolean)
    parking: Mapped[bool | None] = mapped_column(Boolean)
    wheelchair_accessible: Mapped[bool | None] = mapped_column(Boolean)
    pet_friendly: Mapped[bool | None] = mapped_column(Boolean)
    kid_friendly: Mapped[bool | None] = mapped_column(Boolean)
    vegetarian: Mapped[bool | None] = mapped_column(Boolean)
    vegan: Mapped[bool | None] = mapped_column(Boolean)
    halal: Mapped[bool | None] = mapped_column(Boolean)
    alcohol: Mapped[bool | None] = mapped_column(Boolean)
    drive_through: Mapped[bool | None] = mapped_column(Boolean)
    all_day: Mapped[bool | None] = mapped_column(Boolean)
    live_music: Mapped[bool | None] = mapped_column(Boolean)

class Restaurant_Statistics(Base):
    __tablename__ = "restaurant_statistics"

    restaurant_id: Mapped[str] = mapped_column(String, 
                                    ForeignKey("restaurant.restaurant_id"),
                                    primary_key=True)
    average_menu_price: Mapped[float] = mapped_column(Float)
    most_common_cuisine: Mapped[str] = mapped_column(String,
                                            ForeignKey("cuisine.cuisine_name"))
    average_delivery_time: Mapped[int | None] = mapped_column(Integer)
    popularity_score: Mapped[float | None] = mapped_column(Float)
    estimated_value_score: Mapped[float | None] = mapped_column(Float)
