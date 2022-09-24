from fastapi import Depends, FastAPI

from app.routers import baseingredient
from .routers import product, category

from . import models
from .database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
	title="SlashProject API",
	description="This api is able to create a carbon footprint index for consumable goods. The carbon footprint is only an aproximation!",
	version="0.2.0",
	dependencies=[]
)

app.include_router(product.router)
app.include_router(category.router)
app.include_router(baseingredient.router)

@app.get("/")
async def root():
    return {"message": "Hello World!"}
