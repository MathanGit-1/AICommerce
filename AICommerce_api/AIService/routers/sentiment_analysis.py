from fastapi import APIRouter
from pymongo import MongoClient
from transformers import pipeline
import pandas as pd

router = APIRouter()

# Mongo DB setup
client = MongoClient("mongodb://localhost:27017")
db = client["AICommerceDB"]
collection = db["reviews"]

# Load distilbert pipeline
sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

@router.post("/analyze_sentiment")
def analyze_sentiment():
    data = pd.DataFrame(list(collection.find()))
    data = data.dropna(subset=["review_text"])

    for _, row in data.iterrows():
        result = sentiment_pipeline(row['review_text'])[0]
        sentiment = result['label']
        score = round(result['score'], 4)

        collection.update_one(
            {"_id": row["_id"]},
            {"$set": {"sentiment": sentiment, "confidence": score}}
        )
    return {"message": "Sentiment added to all reviews."}
