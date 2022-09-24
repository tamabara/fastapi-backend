from fastapi import APIRouter, Depends, HTTPException

from ..schemas import Product, ProductBase

router = APIRouter(
    prefix="/product",
    tags=["product"],
    dependencies=[],
    responses={404: {"error": "Not found"}},
)

@router.post("/info", summary="ProductInfo", response_model=Product)
async def get_info(item: ProductBase):
	"""
	Get product information from the api
	"""

	return Product(
		ean="number",
		title="productname",
		description="description",
		category="category",
		carbon_score=50
	)
