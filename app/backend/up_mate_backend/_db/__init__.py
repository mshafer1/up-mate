import functools
import datetime
import pymongo

from up_mate_backend import _config

@functools.lru_cache(maxsize=1)
def _get_mongo_collection():
    conn = pymongo.MongoClient(_config.DB_CONNECTION_STRING, timeoutMS=int(1e3))
    db = conn.get_database("up-mate")
    collection = db.get_collection("messages")
    return collection

class NotFoundError(Exception):
    pass

def add_status(info: dict):
    timestamp = datetime.datetime.now()
    _get_mongo_collection().insert_one({**info, "timestamp":timestamp.astimezone()})

def get_latest_status(user: str):
    newest = _get_mongo_collection().find({"user": user}, {"_id": False}, sort=[('timestamp', pymongo.DESCENDING)], limit=1).to_list()
    if not newest:
        raise NotFoundError()
    
    return newest[0]

print(__name__)

if __name__ == "__main__":
    add_status({"user": "test_user", "pain_level": 5, "notes": "This is not okay."})
    print(get_latest_status("test_user"))
