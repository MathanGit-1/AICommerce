from fastapi import APIRouter
from pymongo import MongoClient
import os

router = APIRouter()

@router.get("/")
def sentiment_summary():
    # Mongo DB setup
    #Enable below 2 lines if you want to use docker-compose for MongoDB
    # MONGO_URI = os.getenv("MONGO_URI", "mongodb://new-mongodb:27017")  # Default to localhost if not set
    # client = MongoClient(MONGO_URI)
        
    client = MongoClient("mongodb://localhost:27017")
    
    db = client["AICommerceDB"]
    reviews = list(db["reviews"].find({"sentiment": {"$exists": True}}))

    total = len(reviews)
    positive = sum(1 for r in reviews if r['sentiment'] == 'POSITIVE')
    negative = total - positive

    return {
        "totalReviews": total,
        "positivePercentage": round((positive / total) * 100, 2) if total else 0,
        "negativePercentage": round((negative / total) * 100, 2) if total else 0
    }
