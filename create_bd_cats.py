from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://<username>:<password>@cluster0.j54nsqb.mongodb.net/Cats_test?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

db = client.book

result_many = db.cats.insert_many(
    [
        {
            "name": "Barsik",
            "age": 3,
            "features": ["ходить в капці", "дає себе гладити", "рудий"]
        },
        {
            "name": "Liza",
            "age": 4,
            "features": ["ходить в лоток", "дає себе гладити", "білий"],
        },
    ]
)

