from fastapi import APIRouter, Depends, HTTPException

from ..models import ProductInfo, Product

router = APIRouter(
    prefix="/product",
    tags=["product"],
    dependencies=[],
    responses={404: {"error": "Not found"}},
)

@router.get("/info", summary="ProductInfo", response_model=Product)
async def get_info(item: ProductInfo):
	"""
	Get product information from the api
	"""

	return {"name": "Productname"}
