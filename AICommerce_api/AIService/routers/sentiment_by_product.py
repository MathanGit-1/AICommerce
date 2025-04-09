from fastapi import APIRouter
from pymongo import MongoClient
from collections import defaultdict
import os

router = APIRouter()

@router.get("/")  # ✅ This is needed
def sentiment_by_product():
    # Access the MongoDB URI from environment variable
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://new-mongodb:27017")  # Default to localhost if not set
    client = MongoClient(MONGO_URI)
    db = client["AICommerceDB"]
    reviews = db["reviews"].find({"sentiment": {"$exists": True}})

    product_sentiments = defaultdict(lambda: {"POSITIVE": 0, "NEGATIVE": 0})

    for r in reviews:
        product_id = r.get("product_id", "unknown")
        sentiment = r["sentiment"]
        product_sentiments[product_id][sentiment] += 1

    result = []
    for product, counts in product_sentiments.items():
        total = counts["POSITIVE"] + counts["NEGATIVE"]
        result.append({
            "product_id": product,
            "positive": counts["POSITIVE"],
            "negative": counts["NEGATIVE"],
            "positivePercentage": round((counts["POSITIVE"] / total) * 100, 2) if total else 0
        })

    return result
