from fastapi import APIRouter, Depends, HTTPException

from ..models import ProductInfo, Product

router = APIRouter(
    prefix="/product",
    tags=["product"],
    dependencies=[],
    responses={404: {"error": "Not found"}},
)

@router.get("/info", response_model=Product)
async def get_info(item: ProductInfo):
    return {"name": "Productname"}
