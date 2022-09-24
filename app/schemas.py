from typing import List, Union
from pydantic import BaseModel, Field


# BaseIngedeient Schemas
## ---------- Base Ingredient ----------
class BaseIngredientBase(BaseModel):
	name: str
	name_de: str
	co2_for_100g_without_air: float
	land_transport: float
	sea_transport: float
	air_transport: float
	energy_in_kcal_for_100g: float
	category_id: Union[int, None]

class BaseIngredientCreate(BaseIngredientBase):
	pass

class BaseIngredient(BaseIngredientBase):
	id: int

	class Config:
		orm_mode = True
## -------------------------------------
## ---------- Category ----------
class CategoryBase(BaseModel):
	name: str

class CategoryCreate(CategoryBase):
	pass

class Category(CategoryBase):
	id: int
	base_ingredients: List[BaseIngredient] = []

	class Config:
		orm_mode = True
## ------------------------------


# Product Schemas
class ProductBase(BaseModel):
	ean: str

class Product(ProductBase):
	title: str
	category: str
	nutri_score: str
	carbon_score: int = Field(title="CarbonScore", description="This value is the carbon score", gt=0, le=100)

	class Config:
		orm_mode = True