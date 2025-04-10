from pymongo import MongoClient
import pandas as pd
import numpy as np
import os
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Embedding, Dot, Flatten
from sklearn.model_selection import train_test_split

class ProductRecommendationModel:

    def get_recommendations(user_id: str):
        
        # Access the MongoDB URI from environment variable

        #Enable below 2 lines if you want to use docker-compose for MongoDB
        # MONGO_URI = os.getenv("MONGO_URI", "mongodb://new-mongodb:27017")  # Default to localhost if not set
        # client = MongoClient(MONGO_URI)
        
        client = MongoClient("mongodb://localhost:27017")
        db = client["AICommerceDB"]
        collection = db["user_interactions"]
        print("🔁 Inside productRecommendation")

        records = list(collection.find())
        df = pd.DataFrame(records)

        print("🧾 Columns in DataFrame:", df.columns.tolist())
        print("📄 First 5 records:\n", df.head())

        event_score_map = {
            "view": 1,
            "add_to_cart": 3,
            "purchase": 5
        }

        df = df[df["event_type"].isin(event_score_map)]
        df["interaction"] = df["event_type"].map(event_score_map)
        df["user_code"] = df["user_id"].astype("category").cat.codes
        df["product_code"] = df["product_id"].astype("category").cat.codes

        user_id_map = dict(zip(df["user_code"], df["user_id"]))
        product_id_map = dict(zip(df["product_code"], df["product_id"]))

        n_users = df["user_code"].nunique()
        n_products = df["product_code"].nunique()

        X = df[["user_code", "product_code"]].values
        y = df["interaction"].values

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        user_input = Input(shape=(1,))
        product_input = Input(shape=(1,))
        user_embed = Embedding(input_dim=n_users, output_dim=50)(user_input)
        product_embed = Embedding(input_dim=n_products, output_dim=50)(product_input)
        user_vec = Flatten()(user_embed)
        product_vec = Flatten()(product_embed)
        dot_product = Dot(axes=1)([user_vec, product_vec])
        model = Model([user_input, product_input], dot_product)
        model.compile(loss='mse', optimizer='adam')

        model.fit([X_train[:, 0], X_train[:, 1]], y_train,
                  validation_data=([X_test[:, 0], X_test[:, 1]], y_test),
                  epochs=5, batch_size=64, verbose=0)

        user_df = df[df["user_id"] == user_id]
        if user_df.empty:
            print(" User not found.")
            return []

        user_code = user_df["user_code"].iloc[0]
        all_product_codes = np.arange(n_products)

        purchased_product_codes = df[
            (df["user_code"] == user_code) & (df["event_type"] == "purchase")
        ]["product_code"].unique()

        filtered_product_codes = [code for code in all_product_codes if code not in purchased_product_codes]
        filtered_user_vector = np.full_like(filtered_product_codes, user_code)

        preds = model.predict([filtered_user_vector, np.array(filtered_product_codes)], verbose=1)

        top_indices = np.argsort(preds[:, 0])[::-1]
        sorted_product_codes = np.array(filtered_product_codes)[top_indices]
        sorted_scores = preds[top_indices, 0]

        top_product_codes = sorted_product_codes[:5]
        top_scores = sorted_scores[:5]
        recommended_products = [product_id_map[code] for code in top_product_codes]

        print("\n Top 5 Recommendations with Scores:\n")
        for i in range(5):
            product_id = product_id_map[top_product_codes[i]]
            score = top_scores[i]
            print(f"Product ID: {product_id} | Predicted Interaction Score: {score:.4f}")

        products_collection = db["products"]
        product_details = list(products_collection.find({"product_id": {"$in": recommended_products}}))

        product_scores_map = dict(zip(recommended_products, top_scores))
        for product in product_details:
            product["id"] = str(product.pop("_id", ""))
            product["score"] = float(round(product_scores_map.get(product["product_id"], 0), 4))

        print("Final Recommended Product Details:", product_details)
        return product_details
