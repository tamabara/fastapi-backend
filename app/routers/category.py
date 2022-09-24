from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import SessionLocal
from .. import schemas, models, crud

router = APIRouter(
    prefix="/categories",
    tags=["categories"],
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
@router.post("/", summary="CreateCategory", response_model=schemas.Category)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
	"""
	Create new category
	"""

	db_category = crud.get_category(db, name=category.name)
	if db_category:
		raise HTTPException(status_code=400, detail="Category already exists")
	return crud.create_category(db, category=category)

# READ
@router.get("/", summary="ReadCategories", response_model=List[schemas.Category])
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
	"""
	Read categories
	"""

	return crud.get_categorys(db, skip=skip, limit=limit)

@router.get("/{category_id}", summary="ReadCategory", response_model=schemas.Category)
def read_category(category_id: int, db: Session = Depends(get_db)):
	"""
	Read category
	"""

	db_category = crud.get_category(db, category_id=category_id)
	if db_category is None:
		raise HTTPException(status_code=404, detail="Category not found")
	return db_category

# UPDATE
@router.put("/{category_id}", summary="UpdateCategory", response_model=schemas.Category)
def update_category(category_id: int, category: schemas.CategoryCreate, db: Session = Depends(get_db)):
	"""
	Update Category
	"""

	db_category = crud.update_category(db, category_id=category_id, name=category.name)
	if db_category is None:
		raise HTTPException(status_code=404, detail="Category not found")
	return db_category

# DELETE
@router.delete("/{category_id}", summary="DeleteCategory")
def delete_category(category_id: int, db: Session = Depends(get_db)):
	"""
	Delete Category
	"""

	if crud.delete_category(db, category_id=category_id):
		return {"success": True}
	return {"success": False}
