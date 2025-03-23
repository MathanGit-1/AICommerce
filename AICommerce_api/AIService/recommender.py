from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class ProductRecommender:
    def __init__(self, products_df):
        self.products_df = products_df
        self.product_id_map = {}
        self.similarity_matrix = None
        self.vectorize()

    def vectorize(self):
        self.products_df['combined_features'] = (
            self.products_df['name'].fillna('') + ' ' +
            self.products_df['brand'].fillna('') + ' ' +
            self.products_df['category'].fillna('')
        )
        tfidf = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = tfidf.fit_transform(self.products_df['combined_features'])
        self.similarity_matrix = cosine_similarity(self.tfidf_matrix, self.tfidf_matrix)
        self.product_id_map = dict(enumerate(self.products_df['product_id']))

    def get_similar_product_details(self, product_id, top_n=5):
        try:
            print("✅ recommender.py loaded with get_similar_product_details")
            idx = self.products_df[self.products_df['product_id'] == product_id].index[0]
            sim_scores = list(enumerate(self.similarity_matrix[idx]))
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:top_n+1]
            
            print(f"\n🔍 Similarity scores for Product ID: {product_id}")
            for i, score in sim_scores:
                pid = self.products_df.iloc[i]['product_id']
                pname = self.products_df.iloc[i]['name']
                print(f" - {pname} (Product ID: {pid}) → Similarity: {score:.4f}")

            similar_indices = [i for i, _ in sim_scores]
            products = self.products_df.iloc[similar_indices].copy()

            # Convert _id ObjectId to string (if present)
            if '_id' in products.columns:
                products['_id'] = products['_id'].astype(str)

            return products.to_dict(orient="records")
        except Exception as e:
            print("❌ Error in get_similar_product_details:", e)
            return []
