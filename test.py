
import pymongo
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://CS411ProjectDatabase:negativeone@testcluster1.gfaawrr.mongodb.net/?retryWrites=true&w=majority")
db = cluster["TestCluster1"]
registered_users = db["RegisteredUsers"]

abc = {"name": "Hsd"}

registered_users.insert_one(abc)