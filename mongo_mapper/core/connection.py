import threading

from pymongo import MongoClient
from pymongo import ReadPreference

import mongo_mapper.config as cfg

_connections = {}
_collections = {}
lock = threading.Lock()


def get_collection(alias, object_name, from_primary=False):
    key = object_name + '|' + str(from_primary)

    if key in _collections:

        return _collections[key]

    else:

        lock.acquire()

        try:

            if key in _collections:
                return _collections[key]

            if alias is None or alias == "":
                alias = "default"

            config = [c for c in cfg.MONGODB_SETTINGS if c["ALIAS"] == alias]

            if len(config) is 0:
                raise Exception("{} alias not found in MONGODB_SETTINGS".format(alias))
            else:
                config = config[0]

            client = MongoClient(config["URL"])

            _connections[key] = client

            if from_primary:
                _collections[key] = client.get_database(config['DB_NAME'], read_preference=ReadPreference.PRIMARY)[object_name]
            else:
                _collections[key] = client.get_database(config['DB_NAME'])[object_name]

            return _collections[key]

        finally:

            lock.release()
