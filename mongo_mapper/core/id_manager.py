from enum import Enum
import uuid
from pymongo import MongoClient, ReturnDocument
from bson.objectid import ObjectId


class IdType(Enum):
    Numeric, Incremental, ObjectId = 1, 2, 3


def get_id(id_type, obj_name=None):
    if id_type is IdType.Numeric:
        _id = uuid.uuid1()
        return _id.int >> 64
    elif id_type is IdType.Incremental:
        #TODO: usar el collecion manager
        client = MongoClient('mongodb://localhost:27017/')
        db = client.test_database
        #Force primary
        collection = db.counters
        result = collection.find_one_and_update(filter={'obj_name': obj_name}, update={"$inc": {'count': 1}}, upsert=True, return_document=ReturnDocument.AFTER)
        return result['count']
    else:
        return ObjectId()


print (get_id(IdType.Numeric, None))
print (get_id(IdType.Incremental, 'Hotel'))
print (get_id(IdType.Incremental, 'Hotel'))
print (get_id(IdType.Incremental, 'Hotel'))
print (get_id(IdType.Incremental, 'Hotel'))

print (get_id(IdType.ObjectId, 'Hotel'))
