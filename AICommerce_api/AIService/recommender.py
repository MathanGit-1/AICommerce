from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class ProductRecommender:
    def __init__(self, products_df):
        self.products_df = products_df
        self.product_id_map = {}
        self.similarity_matrix = None
        self.vectorize()

def vectorize(self):
    # 🧠 Combine relevant product text features into a single string for each product
    self.products_df['combined_features'] = (
        self.products_df['name'].fillna('') + ' ' +        # Fill NaNs with empty strings and combine name
        self.products_df['brand'].fillna('') + ' ' +       # Combine brand
        self.products_df['category'].fillna('')            # Combine category
    )

    # 🧹 Initialize a TF-IDF Vectorizer (removing English stopwords)
    tfidf = TfidfVectorizer(stop_words='english')

    # 🔢 Transform the combined features into a TF-IDF matrix
    self.tfidf_matrix = tfidf.fit_transform(self.products_df['combined_features'])

    # 🔗 Compute the cosine similarity matrix between all product vectors
    self.similarity_matrix = cosine_similarity(self.tfidf_matrix, self.tfidf_matrix)

    # 🗺️ Create a mapping from row index to product_id for future lookup
    self.product_id_map = dict(enumerate(self.products_df['product_id']))


    def get_similar_product_details(self, product_id, top_n=5):
        try:
            # ✅ Debug print to confirm function is called
            print("✅ recommender.py loaded with get_similar_product_details")

            # 🔍 Get the index of the product with the given product_id in the DataFrame
            idx = self.products_df[self.products_df['product_id'] == product_id].index[0]

            # 📊 Get similarity scores for the selected product (row in similarity matrix)
            sim_scores = list(enumerate(self.similarity_matrix[idx]))

            # 🔽 Sort the products by similarity score in descending order and exclude the product itself (index 0)
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:top_n+1]

            # 🖨️ Print the top similar products with their similarity scores
            print(f"\n🔍 Similarity scores for Product ID: {product_id}")
            for i, score in sim_scores:
                pid = self.products_df.iloc[i]['product_id']  # Get similar product ID
                pname = self.products_df.iloc[i]['name']       # Get similar product name
                print(f" - {pname} (Product ID: {pid}) → Similarity: {score:.4f}")

            # 🗂️ Get the indices of the top similar products
            similar_indices = [i for i, _ in sim_scores]

            # 📋 Get the corresponding product details from the DataFrame
            products = self.products_df.iloc[similar_indices].copy()

            # 🔄 If MongoDB _id exists, convert ObjectId to string for serialization
            if '_id' in products.columns:
                products['_id'] = products['_id'].astype(str)

            # 📤 Return the similar product details as a list of dictionaries
            return products.to_dict(orient="records")

        except Exception as e:
            # ⚠️ Catch and print any error that occurs during processing
            print("❌ Error in get_similar_product_details:", e)
            return []