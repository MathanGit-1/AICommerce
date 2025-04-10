from fastapi import APIRouter
from pymongo import MongoClient
from transformers import pipeline
import pandas as pd
import os

router = APIRouter()

# Mongo DB setup
#Enable below 2 lines if you want to use docker-compose for MongoDB
# MONGO_URI = os.getenv("MONGO_URI", "mongodb://new-mongodb:27017")  # Default to localhost if not set
# client = MongoClient(MONGO_URI)
        
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
