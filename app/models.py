from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from .database import Base


# SQLAlchemy Models
class Category(Base):
	__tablename__ = "categories"

	id = Column(Integer, primary_key=True, index=True)
	name = Column(String, unique=True)

	base_ingredients = relationship("BaseIngedient", back_populates="category")

class BaseIngedient(Base):
	__tablename__ = "base_ingedients"

	id = Column(Integer, primary_key=True, index=True)
	name_de = Column(String, unique=True)
	name = Column(String, unique=True)
	co2_for_100g_without_air = Column(Float)
	land_transport = Column(Float)
	sea_transport = Column(Float)
	air_transport = Column(Float)
	energy_in_kcal_for_100g = Column(Float)
	category_id = Column(Integer, ForeignKey("categories.id"))


	category = relationship("Category", back_populates="base_ingredients")
