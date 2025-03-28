from fastapi import FastAPI
from utils.mongo_loader import load_products
from recommender import ProductRecommender
from productRecommendation import ProductRecommendationModel

app = FastAPI()

# below code is get the recommended products using faiss search
# Load and initialize
# products_df = load_products()
# recommender = ProductRecommender(products_df)
# # ✅ Debug line to check available methods
# print("✅ Methods:", dir(recommender))

# print("✅ recommender.py loaded")
# @app.get("/recommend/{product_id}")
# def recommend(product_id: str):
#     product_id = product_id.upper()
#     recommended_products = recommender.get_similar_product_details(product_id)

#     for product in recommended_products:
#         if '_id' in product:
#             product['id'] = product['_id']
#         elif 'product_id' in product:
#             product['id'] = product['product_id']  # <- important!
#             print("\n🧪 Sample product returned to React:")
#             print(recommended_products[0])
#     return { "recommended_products": recommended_products }

@app.get("/AIRecommendedProducts/{user_id}")
def AIRecommendedProducts(user_id:str):
    result = ProductRecommendationModel.get_recommendations(user_id)
    return result
