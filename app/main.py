from fastapi import Depends, FastAPI
from .routers import product

app = FastAPI(dependencies=[])

app.include_router(product.router)

@app.get("/")
async def root():
    return {"message": "Hello World!"}
