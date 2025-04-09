import pandas as pd
from pymongo import MongoClient

#connect to mongo DB
client = MongoClient('localhost', 27018)
db = client['AICommerceDB']

#Load the products data from csv into mongoDB
products_df = pd.read_csv('products.csv')
products_records = products_df.to_dict(orient="records")
db.products.delete_many({})
db.products.insert_many(products_records)
print(f"✅ Inserted {len(products_records)} products.")

# ✅ Load user_interactions_2000.csv
interactions_df = pd.read_csv("user_interactions_2000.csv")
interactions_records = interactions_df.to_dict(orient="records")
db.user_interactions.delete_many({})  # Clear existing records (optional)
db.user_interactions.insert_many(interactions_records)
print(f"✅ Inserted {len(interactions_records)} user interactions.")
