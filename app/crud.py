from typing import Union, List
from sqlalchemy.orm import Session

from . import models, schemas



# Category CRUD
## CREATE -----------------------------------------------------------------
def create_category(db: Session, category: schemas.CategoryCreate) -> models.Category:
	"""
	CREATE a category
	"""

	db_category = models.Category(name=category.name)
	db.add(db_category)
	db.commit()
	db.refresh(db_category)
	return db_category
## ------------------------------------------------------------------------

## READ -------------------------------------------------------------------
def get_category(db: Session, category_id: int = None, name: str = None) -> Union[models.Category, None]:
	"""
	READ one category
	"""

	if category_id is not None:
		return db.query(models.Category).filter(models.Category.id == category_id).first()
	if name is not None:
		return db.query(models.Category).filter(models.Category.name == name).first()
	return None

def get_categorys(db: Session, skip: int = 0, limit: int = 100) -> Union[List[models.Category], None]:
	"""
	READ all categories
	"""

	return db.query(models.Category).offset(skip).limit(limit).all()
## ------------------------------------------------------------------------

## UPDATE -----------------------------------------------------------------
def update_category(db: Session, category_id: int, name: str = None) -> Union[models.Category, None]:
	"""
	UPDATE a category
	"""

	update_dict = {}
	if name is not None:
		update_dict["name"] = name

	if update_dict:
		db.query(models.Category).filter(models.Category.id == category_id).update(update_dict)
		db.commit()
		return db.query(models.Category).filter(models.Category.id == category_id).first()
	return None
## ------------------------------------------------------------------------

## DELETE -----------------------------------------------------------------
def delete_category(db: Session, category_id: int = None, name: str = None) -> bool:
	"""
	DELETE a category
	"""

	if category_id is not None:
		if db.query(models.Category).filter(models.Category.id == category_id).delete() > 0:
			db.commit()
			return True
	if name is not None:
		if db.query(models.Category).filter(models.Category.name == name).delete() > 0:
			db.commit()
			return True
	return False
## ------------------------------------------------------------------------


# BaseIngedient CRUD
## CREATE -----------------------------------------------------------------
def create_baseingredient(db: Session, baseingredient: schemas.BaseIngredientCreate) -> models.BaseIngedient:
	"""
	CREATE a BaseIngredient
	"""

	db_baseingredient = models.BaseIngedient(
		name=baseingredient.name,
		name_de=baseingredient.name_de,
		co2_for_100g_without_air = baseingredient.co2_for_100g_without_air,
		land_transport = baseingredient.land_transport,
		sea_transport = baseingredient.sea_transport,
		air_transport = baseingredient.air_transport,
		energy_in_kcal_for_100g = baseingredient.energy_in_kcal_for_100g,
		category_id = baseingredient.category_id
	)
	db.add(db_baseingredient)
	db.commit()
	db.refresh(db_baseingredient)
	return db_baseingredient
## ------------------------------------------------------------------------

## READ -------------------------------------------------------------------
def get_baseingredient(db: Session, id: int = None, name: str = None, name_de: str = None) -> Union[models.BaseIngedient, None]:
	"""
	READ one BaseIngredient
	"""

	if id is not None:
		return db.query(models.BaseIngedient).filter(models.BaseIngedient.id == id).first()
	if name is not None:
		return db.query(models.BaseIngedient).filter(models.BaseIngedient.name == name).first()
	if name_de is not None:
		return db.query(models.BaseIngedient).filter(models.BaseIngedient.name_de == name_de).first()
	return None

def get_baseingredients(db: Session, skip: int = 0, limit: int = 100) -> Union[List[models.BaseIngedient], None]:
	"""
	READ all BaseIngredient
	"""

	return db.query(models.BaseIngedient).offset(skip).limit(limit).all()
## ------------------------------------------------------------------------

## UPDATE -----------------------------------------------------------------
def update_baseingredient(db: Session, id: int, name: str = None, name_de: str = None) -> Union[models.Category, None]:
	"""
	UPDATE a BaseIngredient
	"""

	######

	update_dict = {}
	if name is not None:
		update_dict["name"] = name
	if name_de is not None:
		update_dict["name_de"] = name_de

	if update_dict:
		db.query(models.BaseIngedient).filter(models.BaseIngedient.id == id).update(update_dict)
		db.commit()
		return db.query(models.BaseIngedient).filter(models.BaseIngedient.id == id).first()
	return None
## ------------------------------------------------------------------------

## DELETE -----------------------------------------------------------------
def delete_baseingredient(db: Session, id: int = None, name: str = None, name_de: str = None) -> bool:
	"""
	DELETE a BaseIngredient
	"""

	if id is not None:
		if db.query(models.BaseIngedient).filter(models.BaseIngedient.id == id).delete() > 0:
			db.commit()
			return True
	if name is not None:
		if db.query(models.BaseIngedient).filter(models.BaseIngedient.name == name).delete() > 0:
			db.commit()
			return True
	if name_de is not None:
		if db.query(models.BaseIngedient).filter(models.BaseIngedient.name_de == name_de).delete() > 0:
			db.commit()
			return True
	return False
## ------------------------------------------------------------------------