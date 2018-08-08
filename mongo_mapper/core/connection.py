from pymongo import MongoClient
from mongo_mapper.config import MONGODB_SETTINGS

_connections = {}
_collections = {}


def get_collection(alias, object_name):
    if object_name not in _collections:
        if alias is None or alias == "":
            alias = "default"

        config = [c for c in MONGODB_SETTINGS if c["ALIAS"] == alias]
        if len(config) is 0:
            raise Exception("{} alias not found in MONGODB_SETTINGS".format(alias))
        else:
            config = config[0]

        client = MongoClient(config["URL"])
        _connections[alias] = client
        _collections[object_name] = client[client._MongoClient__default_database_name][object_name]

    return _collections[object_name]
