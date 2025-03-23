from pymongo import MongoClient
import pandas as pd

def load_products():
    client = MongoClient('localhost', 27017)
    db = client['AICommerceDB']
    products_cursor = db['products'].find()
    return pd.DataFrame(products_cursor)
