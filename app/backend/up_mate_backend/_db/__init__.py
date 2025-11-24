import datetime
import pymongo

from up_mate_backend import _config

_conn = pymongo.MongoClient(_config.DB_CONNECTION_STRING)

_db = _conn.get_database("up-mate")

_collection = _db.get_collection("messages")

class NotFoundError(Exception):
    pass

def add_status(info: dict):
    timestamp = datetime.datetime.now()
    _collection.insert_one({**info, "timestamp":timestamp.astimezone()})

def get_latest_status(user: str):
    newest = _collection.find({"user": user}, {"_id": False}, sort=[('timestamp', pymongo.DESCENDING)], limit=1).to_list()
    if not newest:
        raise NotFoundError()
    
    return newest[0]
