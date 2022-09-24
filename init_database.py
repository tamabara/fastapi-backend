from nis import cat
import os
import csv
from app import models, database, crud, schemas

filepath = "./data.db"
datacsv = "./data.csv"

# remove databse
if os.path.isfile(filepath):
	os.remove(filepath)

models.Base.metadata.create_all(bind=database.engine)

db = database.SessionLocal()

csvfile = open(datacsv, newline='')
reader = csv.DictReader(csvfile)

for row in reader:
	if crud.get_category(db, name=row["category"]) is None:
		category = crud.create_category(db, schemas.CategoryCreate(
			name=row["category"]
		))

csvfile.close()

print("Finished Categories...")

csvfile = open(datacsv, newline='')
reader = csv.DictReader(csvfile)

for row in reader:
	if crud.get_baseingredient(db, name=row["name"]) is None:
		cat_id = crud.get_category(db, name=row["category"])

		baseingredient = crud.create_baseingredient(
			db,
			schemas.BaseIngredientCreate(
				name=row["name"],
				name_de=row["name_de"],
				co2_for_100g_without_air=row["co2_for_100g_without_air"],
				land_transport=row["land_transport"],
				sea_transport=row["sea_transport"],
				air_transport=row["air_transport"],
				energy_in_kcal_for_100g=row["energy_in_kcal"],
				category_id=cat_id.id
			)
		)

print("Finished BaseIngredients...")

csvfile.close()
