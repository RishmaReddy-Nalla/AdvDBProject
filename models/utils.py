from pymongo import MongoClient
import os

class MongoConn:
    def __init__(self):
        self.username = os.getenv('MONGO_USER')
        self.password = os.getenv('MONGO_PASS')
    
    def connect(self):
        try:
            client = MongoClient(f'mongodb+srv://{self.username}:{self.password}@hmsd.oajv2rn.mongodb.net/?retryWrites=true&w=majority&appName=HMSD')
            db = client['HMSD']
            # collection = db[self.collection]
            return db
        except Exception as e:
            return f"Failed to connect to Mongo Server Check your connection string {e}"
        