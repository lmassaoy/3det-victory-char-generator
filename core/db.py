from bson import ObjectId
from pymongo import MongoClient


def get_database(): 
    CONNECTION_STRING = "mongodb://root:example@localhost:27017/"
    client = MongoClient(CONNECTION_STRING)
    return client['app_db']


def get_collection(collection_name: str):
    db =  get_database()
    if collection_name not in db.list_collection_names():
        collection_client = db[collection_name]
        dummy_id = collection_client.insert_one({'empty': 'empty'}).inserted_id
        collection_client.delete_one({'_id': ObjectId(dummy_id)})

    return db[collection_name]