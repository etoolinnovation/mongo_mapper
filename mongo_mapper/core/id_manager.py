from enum import Enum
import uuid
from pymongo import ReturnDocument
from bson.objectid import ObjectId
from mongo_mapper.core.connection import get_collection


class IdType(Enum):
    Numeric, Incremental, ObjectId = 1, 2, 3


def get_id(id_type, obj_name=None):
    if id_type is IdType.Numeric:
        _id = uuid.uuid1()
        return _id.int >> 64
    elif id_type is IdType.Incremental:

        collection = get_collection('', 'counters', True)
        result = collection.find_one_and_update(filter={'obj_name': obj_name}, update={"$inc": {'count': 1}}, upsert=True, return_document=ReturnDocument.AFTER)
        return result['count']
    else:
        return ObjectId()
