from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import json

uri = "mongodb+srv://<username>:<password>@cluster0.j54nsqb.mongodb.net/Cats_test?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

db = client["qoutes_db"]

authors_collection = db["authors"]
quotes_collection = db["quotes"]

# Import authors data
with open("authors.json", "r", encoding="utf-8") as f:
    authors_data = json.load(f)
    authors_collection.insert_many(authors_data)

# Import quotes data
with open("quotes.json", "r", encoding="utf-8") as f:
    quotes_data = json.load(f)
    quotes_collection.insert_many(quotes_data)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
