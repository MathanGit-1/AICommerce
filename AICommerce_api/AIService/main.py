from fastapi import FastAPI
from productRecommendation import ProductRecommendationModel
from routers import sentiment_summary, sentiment_by_product
from routers import sentiment_analysis

app = FastAPI()

# 👇 Existing AI recommendation endpoint
@app.get("/AIRecommendedProducts/{user_id}")
def AIRecommendedProducts(user_id: str):
    result = ProductRecommendationModel.get_recommendations(user_id)
    return result

# 👇 Include only sentiment-related routers
app.include_router(sentiment_summary.router, prefix="/sentiment_summary")
app.include_router(sentiment_by_product.router, prefix="/sentiment_analysis")
app.include_router(sentiment_by_product.router, prefix="/sentiment_by_product")
app.include_router(sentiment_analysis.router, prefix="/sentiment")