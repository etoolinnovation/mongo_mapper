import uuid
from enum import Enum

from bson.int64 import Int64
from bson.objectid import ObjectId
from pymongo import ReturnDocument

from mongo_mapper.core.cache import get_collection


class IdType(Enum):
    Numeric, Incremental, ObjectId = 1, 2, 3


def get_id(id_type, obj_name=None, range_ids=None):
    if id_type is IdType.Numeric:
        if range_ids is None:
            _id = uuid.uuid1()
            return Int64(_id.int >> 64)
        else:
            ids = []
            for x in range(0, range_ids):
                _id = uuid.uuid1()
                ids.append(Int64(_id.int >> 64))
            return ids

    elif id_type is IdType.Incremental:

        collection = get_collection('', 'counters', True)
        result = collection.find_one_and_update(filter={'obj_name': obj_name},
                                                update={"$inc": {'count': range_ids if range_ids is not None else 1}},
                                                upsert=True, return_document=ReturnDocument.AFTER)
        if range_ids is None:
            return result['count']
        else:
            return list(range(result['count'] - range_ids, result['count']))

    else:
        if range_ids is None:
            return ObjectId()
        else:
            ids = []
            for x in range(0, range_ids):
                ids.append(ObjectId())
            return ids
