from typing import List
from math import prod
from unittest import result
from urllib import request
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import openfoodfacts
from fuzzywuzzy import fuzz
from statistics import median
import requests
from bs4 import BeautifulSoup

from ..database import SessionLocal
from ..schemas import Product, ProductBase
from .. import models, crud

router = APIRouter(
    prefix="/product",
    tags=["product"],
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
			

def	get_ingredients(db: Session, ean: str, min_match: int):
	product = openfoodfacts.products.get_product(ean)
	if product is not None:
		product = dict(product["product"])

	ingredients = product.get("ingredients")
	ingredient_results = {}
	if ingredients is not None:
		baseingredients = [{"id": i.id, "name": i.name_de} for i in crud.get_baseingredients(db, limit=500)]
		for index, ingredient in enumerate(ingredients):
			lastmatch = None
			lastmatch_val = 0
			for baseingredient in baseingredients:
				matchratio = fuzz.token_sort_ratio(baseingredient["name"], ingredient.get("text"))
				if matchratio >= min_match and matchratio > lastmatch_val:
					lastmatch_val = matchratio
					lastmatch = baseingredient
				matchratio = fuzz.partial_ratio(baseingredient["name"], ingredient.get("text"))
				if matchratio >= min_match and matchratio > lastmatch_val:
					lastmatch_val = matchratio
					lastmatch = baseingredient
				matchratio = fuzz.token_set_ratio(baseingredient["name"], ingredient.get("text"))
				if matchratio >= min_match and matchratio > lastmatch_val:
					lastmatch_val = matchratio
					lastmatch = baseingredient
			if lastmatch is not None:
				ingredient_results[index] = crud.get_baseingredient(db, id=lastmatch["id"])
	ingredient_results1 = dict(ingredient_results)
	ingredient_results2 = dict(ingredient_results)
	for keyout, ingredientout in ingredient_results1.items():
		for keyin, ingredientin in ingredient_results2.items():
			if fuzz.partial_ratio(ingredientout.name_de, ingredientin.name_de) > 80 and ingredientout is not ingredientin:
				outcarb1 = ingredientout.co2_for_100g_without_air
				transportation = [i for i in [ingredientout.air_transport, ingredientout.sea_transport, ingredientout.land_transport] if i > 0]
				if transportation:
					outcarb1 += median(transportation)
				outcarb2 = ingredientout.co2_for_100g_without_air
				transportation = [i for i in [ingredientin.air_transport, ingredientin.sea_transport, ingredientin.land_transport] if i > 0]
				if transportation:
					outcarb2 += median(transportation)
				if outcarb1 > outcarb2:
					if keyin in ingredient_results:
						ingredient_results.pop(keyin)
				else:
					if keyout in ingredient_results:
						ingredient_results.pop(keyout)
	
	return (
		product.get("product_name"),
		product.get("ingredients"),
		ingredient_results,
		product.get("nutriscore_grade"),
		product.get("categories_old"),
		str(product.get("brands")).split(", ")
	)

def carbon_calulator(ingredients: List[dict], baseingredients: dict):
	total_carb = 0.0
	for key, ingredient in enumerate(ingredients):
		if key in baseingredients:
			baseingredient = baseingredients[key]
			carb = ingredient.get("percent_estimate") * (baseingredient.co2_for_100g_without_air / 100)
			transportation = [i for i in [baseingredient.air_transport, baseingredient.sea_transport, baseingredient.land_transport] if i > 0]
			if transportation:
				carb += ingredient.get("percent_estimate") * (median(transportation) / 100)
			total_carb += carb
	return total_carb

def create_carbon_score(co2_per_100g: int):
	BADDEST_CO2_GRAMMS = 500
	percentage = (co2_per_100g / BADDEST_CO2_GRAMMS) * 100
	if percentage > 0.0:
		percentage = 100.0 - round(percentage if percentage <= 100.0 else 100.0)
		return percentage if percentage > 0.0 else 1.0
	return 100.0

def get_image(ean: str):
	response = requests.get(
		f"https://de.images.search.yahoo.com/search/images?p=ean%3A+{ean}",
		headers={
			"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15"
		}
	)
	soup = BeautifulSoup(response.content, "lxml")
	urls = [item.find('img')["data-src"] for item in soup.find(id="sres").find_all("li")]
	return urls[0] if len(urls) > 0 else None


@router.post("/info", summary="ProductInfo", response_model=Product)
async def get_info(item: ProductBase, db: Session = Depends(get_db)):
	"""
	Get product information from the api
	"""

	name, ingredients, baseingredients, nutriscore, category, brands = get_ingredients(db, item.ean, 85)
	co2_per_100g = carbon_calulator(ingredients, baseingredients)
	carbon_score = create_carbon_score(co2_per_100g)
	img_src = get_image(ean=item.ean)

	return Product(
		ean=item.ean,
		title=name,
		category=category,
		nutri_score=nutriscore,
		image_url=img_src,
		brands=brands,
		carbon_score=carbon_score
	)
