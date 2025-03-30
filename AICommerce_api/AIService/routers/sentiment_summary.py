from fastapi import APIRouter
from pymongo import MongoClient

router = APIRouter()

@router.get("/")
def sentiment_summary():
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
