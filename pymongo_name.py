import pymongo
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://cindyjin03:1234@cluster0.yy8tl5m.mongodb.net/?retryWrites=true&w=majority")
db = cluster["test"]
collection = db["test"]

post = {"_id": 0, "name": "tim"}

collection.insert_one(post)