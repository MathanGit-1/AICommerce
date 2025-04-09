import pandas as pd
from pymongo import MongoClient

# MongoDB Connection
client = MongoClient('localhost', 27018)
db = client['AICommerceDB']  # Connect to your database

# User IDs List
user_ids = [
    "U035", "U042", "U031", "U018", "U017", "U010", "U018", "U005", "U007", "U023",
    "U031", "U039", "U030", "U025", "U005", "U007", "U021", "U003", "U022", "U025",
    "U005", "U030", "U029", "U037", "U003", "U021", "U026", "U029", "U020", "U014",
    "U040", "U008", "U020", "U007", "U008", "U045", "U020", "U033", "U014", "U005",
    "U032", "U010", "U024", "U034", "U037", "U010", "U027", "U007", "U019", "U010",
    "U044", "U001", "U048", "U010", "U034", "U008", "U004", "U006", "U020", "U034",
    "U029", "U050", "U050", "U031", "U005", "U001", "U006", "U011", "U021", "U022",
    "U023", "U014", "U049", "U002", "U032", "U026", "U014", "U019", "U028", "U050",
    "U009", "U021", "U001", "U009", "U008", "U045", "U007", "U036", "U013", "U007",
    "U002", "U033", "U029", "U036", "U033", "U004", "U035", "U021", "U005", "U035",
    "U045", "U041", "U008", "U022", "U050", "U008", "U020", "U008", "U046", "U006",
    "U046", "U036", "U038", "U046", "U020"
]

# Generate user data (for now we will just use user ID)
users = [{"user_id": user_id, "name": f"User {user_id}", "status": "active"} for user_id in user_ids]

# Insert the data into MongoDB (you can clear existing data if needed)
db.users.delete_many({})  # Optional: Remove existing documents
db.users.insert_many(users)  # Insert the users into the collection

print(f"✅ Inserted {len(users)} users into the database.")