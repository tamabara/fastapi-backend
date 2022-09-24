from fastapi import Depends, FastAPI
from .routers import product

app = FastAPI(
	title="SlashProject API",
	description="This api is able to create a carbon footprint index for consumable goods. The carbon footprint is only an aproximation!",
	version="0.1.0",
	dependencies=[]
)

app.include_router(product.router)

@app.get("/")
async def root():
    return {"message": "Hello World!"}
