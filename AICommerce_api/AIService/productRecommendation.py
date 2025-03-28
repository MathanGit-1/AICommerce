# Required libraries
from pymongo import MongoClient
import pandas as pd
import numpy as np
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Embedding, Dot, Flatten
from sklearn.model_selection import train_test_split

class ProductRecommendationModel:

    def get_recommendations(user_id: str):
        # 🔹 STEP 1: Connect to MongoDB and Load Data
        # ------------------------------------------
        # We fetch all user-product interaction data from MongoDB
        client = MongoClient("mongodb://localhost:27017")  # Adjust if hosted differently
        db = client["AICommerceDB"]
        collection = db["user_interactions"]
        print("inside productRecommendation")
        # Get all documents from the userinteractions collection
        records = list(collection.find())

        # Convert the list of documents into a pandas DataFrame for processing
        df = pd.DataFrame(records)
        # 🔍 Debug print
        print("Columns in DataFrame:", df.columns.tolist())
        print("First 5 records:\n", df.head())
        # 🔹 STEP 2: Preprocess the Data
        # -----------------------------
        # Map each event_type (view, click, purchase...) to a numeric score representing interaction strength
        event_score_map = {
            "view": 1,
            "add_to_cart": 3,
            "purchase": 5
        }
        print(df.head())
        # Remove any events we don't care about
        df = df[df["event_type"].isin(event_score_map)]

        # Create a new column "interaction" based on event_type score
        df["interaction"] = df["event_type"].map(event_score_map)

        # Encode user_id and product_id into numerical codes starting from 0
        # This is needed because embedding layers only accept integers starting from 0
        df["user_code"] = df["user_id"].astype("category").cat.codes
        df["product_code"] = df["product_id"].astype("category").cat.codes

        # Save mappings to convert numeric predictions back to actual product_ids
        user_id_map = dict(zip(df["user_code"], df["user_id"]))
        product_id_map = dict(zip(df["product_code"], df["product_id"]))

        # Count the number of unique users and products — used for embedding dimensions
        n_users = df["user_code"].nunique()
        n_products = df["product_code"].nunique()

        # Create training inputs (X) and output labels (y)
        X = df[["user_code", "product_code"]].values  # Inputs to the model
        y = df["interaction"].values  # Target value to predict (interaction strength)

        # Split into training and testing datasets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # 🔹 STEP 3: Build the Neural Collaborative Filtering Model
        # --------------------------------------------------------

        # Input layer for user
        user_input = Input(shape=(1,))
        # Input layer for product
        product_input = Input(shape=(1,))

        # Embedding layer for users: each user gets a 50-dimensional vector
        user_embed = Embedding(input_dim=n_users, output_dim=50)(user_input)

        # Embedding layer for products: each product gets a 50-dimensional vector
        product_embed = Embedding(input_dim=n_products, output_dim=50)(product_input)

        # Flatten the embedding vectors to 1D
        user_vec = Flatten()(user_embed)
        product_vec = Flatten()(product_embed)

        # Dot product of user and product vectors gives a predicted interaction score
        dot_product = Dot(axes=1)([user_vec, product_vec])

        # Define the final model
        model = Model([user_input, product_input], dot_product)

        # Compile the model with Mean Squared Error (MSE) loss
        model.compile(loss='mse', optimizer='adam')

        # 🔹 STEP 4: Train the Model
        # -------------------------
        # Fit the model on the training data (we keep epochs low to avoid long training during development)
        model.fit([X_train[:, 0], X_train[:, 1]], y_train,
                  validation_data=([X_test[:, 0], X_test[:, 1]], y_test),
                  epochs=5, batch_size=64, verbose=0)

        # 🔹 STEP 5: Predict & Recommend for a Given User
        # ----------------------------------------------

        # First, map the incoming user_id (like 35) to its encoded form (like 2)
        user_df = df[df["user_id"] == user_id] # Assuming user_id format like U035
        if user_df.empty:
            return []  # If user not found in data, return empty list

        user_code = user_df["user_code"].iloc[0]

        # Create a list of all product codes for prediction
        all_product_codes = np.arange(n_products)

        # Prepare a user array same length as products for batch prediction
        #user_vector = np.full_like(all_product_codes, user_code)
    
        #Get product codes the user already has purchased'
        purchased_product_codes = df[(df["user_code"] == user_code) & (df["event_type"] == "purchase")]["product_code"].unique()

        #Filter only unpurchased product codes
        filtered_product_codes = [code for code in all_product_codes if code not in purchased_product_codes]
    
        filtered_user_vector = np.full_like(filtered_product_codes, user_code)
        # Predict interaction scores for all products for this user
        preds = model.predict([filtered_user_vector, np.array(filtered_product_codes)], verbose=1)

        # Sort product codes by predicted score (highest first)
        top_indices = np.argsort(preds[:, 0])[::-1][:5]  # Top 5 products
        top_product_codes = all_product_codes[top_indices]
        
        # Convert back the numeric product codes to original product_id
        recommended_products = [product_id_map[code] for code in top_product_codes]
        print("Recommended Products:", recommended_products)

        #Get the full product details from the products collection
        products_collection = db["products"]

        # 🔹 Fetch full product details for the recommended product_ids
        product_details = list(products_collection.find({"product_id": {"$in": recommended_products}}))
        
        # 🔹 Optional: Convert ObjectId to string for clean JSON
        for product in product_details:
            product["id"] = str(product.pop("_id", ""))  # Rename _id to id

        # 🔹 Debug print
        print("🧪 Final Recommended Product Details:", product_details)

        return product_details
