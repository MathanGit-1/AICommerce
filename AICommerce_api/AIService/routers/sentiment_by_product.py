from fastapi import APIRouter
from pymongo import MongoClient
from collections import defaultdict
import os

router = APIRouter()

@router.get("/")
def sentiment_by_product():
    # Mongo DB setup
    #Enable below 2 lines if you want to use docker-compose for MongoDB
    # MONGO_URI = os.getenv("MONGO_URI", "mongodb://new-mongodb:27017")  # Default to localhost if not set
    # client = MongoClient(MONGO_URI)
    client = MongoClient("mongodb://localhost:27017")
    db = client["AICommerceDB"]

    reviews = db["reviews"].find({"sentiment": {"$exists": True}})
    products_collection = db["products"]

    product_sentiments = defaultdict(lambda: {"POSITIVE": 0, "NEGATIVE": 0})
    product_names = {}

    for r in reviews:
        product_id = r.get("product_id", "unknown")
        sentiment = r["sentiment"]
        product_sentiments[product_id][sentiment] += 1

        # Fetch product name once per product_id
        if product_id not in product_names:
            product = products_collection.find_one({"product_id": product_id})
            product_names[product_id] = product["name"] if product and "name" in product else product_id

    result = []
    for product_id, counts in product_sentiments.items():
        total = counts["POSITIVE"] + counts["NEGATIVE"]
        result.append({
            "product_id": product_id,
            "product_name": product_names[product_id],
            "positive": counts["POSITIVE"],
            "negative": counts["NEGATIVE"],
            "positivePercentage": round((counts["POSITIVE"] / total) * 100, 2) if total else 0
        })

    return result