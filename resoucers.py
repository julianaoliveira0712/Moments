import pymongo

client = pymongo.MongoClient("mongodb+srv://remember_auth:hRmXnjYiziGTz3DP@cluster0-d2d9w.azure.mongodb.net/test?retryWrites=true&w=majority")
db = client["remember-dev"]