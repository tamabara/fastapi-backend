from fastapi import APIRouter, Depends, HTTPException

import openfoodfacts

from ..schemas import Product, ProductBase

router = APIRouter(
    prefix="/product",
    tags=["product"],
    dependencies=[],
    responses={404: {"error": "Not found"}},
)

def	get_ingredients(ean: str):
	product = openfoodfacts.products.get_product(ean)
	return (
		product["product"]["product_name"],
		str(product["product"]["ingredients_text"]).split(", "),
		product["product"]["nutriscore_grade"]
	)

@router.post("/info", summary="ProductInfo", response_model=Product)
async def get_info(item: ProductBase):
	"""
	Get product information from the api
	"""

	name, ingredients, nutriscore = get_ingredients(item.ean)

	return Product(
		ean=item.ean,
		title=name,
		category="category",
		nutri_score=nutriscore,
		carbon_score=50
	)
