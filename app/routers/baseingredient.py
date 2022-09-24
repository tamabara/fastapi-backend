from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import SessionLocal
from .. import schemas, models, crud

router = APIRouter(
    prefix="/baseingretients",
    tags=["baseingretients"],
    dependencies=[],
    responses={404: {"error": "Not found"}},
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CREATE
@router.post("/", summary="CreateBaseIngredient", response_model=schemas.BaseIngredient)
def create_baseingredient(baseingredient: schemas.BaseIngredientCreate, db: Session = Depends(get_db)):
	"""
	Create new BaseIngredient
	"""

	category_id = crud.get_category(db, category_id=baseingredient.category_id)

	if category_id is None:
		baseingredient.category_id = None

	db_baseingredient = crud.get_baseingredient(db, name=baseingredient.name)
	if db_baseingredient:
		raise HTTPException(status_code=400, detail="BaseIngredient already exists")
	return crud.create_baseingredient(db, baseingredient=baseingredient)

# READ
@router.get("/", summary="ReadBaseIngredients", response_model=List[schemas.BaseIngredient])
def read_baseingredient(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
	"""
	Read BaseIngredient
	"""

	return crud.get_baseingredients(db, skip=skip, limit=limit)

@router.get("/{id}", summary="ReadBaseIngredient", response_model=schemas.BaseIngredient)
def read_baseingredient(id: int, db: Session = Depends(get_db)):
	"""
	Read BaseIngredient
	"""

	db_baseingredient = crud.get_baseingredient(db, id=id)
	if db_baseingredient is None:
		raise HTTPException(status_code=404, detail="BaseIngredient not found")
	return db_baseingredient

# UPDATE
@router.put("/{category_id}", summary="UpdateBaseIngredient", response_model=schemas.BaseIngredient)
def update_baseingredient(id: int, baseingredient: schemas.BaseIngredientCreate, db: Session = Depends(get_db)):
	"""
	Update BaseIngredient
	"""

	db_category = crud.update_baseingredient(db, id=id, name=baseingredient.name)
	if db_category is None:
		raise HTTPException(status_code=404, detail="BaseIngredient not found")
	return db_category

# DELETE
@router.delete("/{category_id}", summary="DeleteBaseIngredient")
def delete_baseingredient(id: int, db: Session = Depends(get_db)):
	"""
	Delete BaseIngredient
	"""

	if crud.delete_baseingredient(db, id=id):
		return {"success": True}
	return {"success": False}
