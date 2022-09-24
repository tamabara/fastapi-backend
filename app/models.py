from pydantic import BaseModel


class ProductInfo(BaseModel):
	ean: str

class Product(BaseModel):
	ean: str
