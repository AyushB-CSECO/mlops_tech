from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pathlib import Path

from database import Base

# # Reset to Base Folder
# FILE_PATH = Path(__file__).resolve()
# BASE_PATH = FILE_PATH.parent.parent.parent

class Country(Base):
    __tablename__ = "country"
    
    country: Mapped[str] =  mapped_column(String, primary_key=True)
    region: Mapped[str | None] = mapped_column(String)
    income_group: Mapped[str | None] = mapped_column(String)
    currency: Mapped[str] = mapped_column(String, unique=True)
    timezone: Mapped[str | None] = mapped_column(String) 
    iso_code: Mapped[str | None] = mapped_column(String, unique=True)





if __name__ == "__main__":
    print("All libraries imported successfully.")
