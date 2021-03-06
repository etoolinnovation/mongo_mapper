import threading
import types

from pymongo import MongoClient
from pymongo import ReadPreference

import mongo_mapper.config as cfg
from mongo_mapper.exceptions import TypeListNotFound

_connections = {}
_collections = {}
_documents_type = {}
lock = threading.Lock()


def get_collection(alias, object_name, from_primary=False, context=""):
    key = object_name + '|' + str(from_primary) + '|' + context

    if key in _collections:

        return _collections[key]

    else:

        lock.acquire()

        try:

            if key in _collections:
                return _collections[key]

            if alias is None or alias == "":
                alias = "default"

            config = [c for c in cfg.MONGODB_SETTINGS[context] if c["ALIAS"] == alias]

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


def get_meta(document_class, document_name):

    key = document_name + "|" + document_class.__module__

    if key in _documents_type and "meta" in _documents_type[key]:

        return _documents_type[key]["meta"]

    else:

        lock.acquire()

        try:

            meta = document_class._meta if hasattr(document_class, "_meta") else {}

            if key not in _documents_type:
                _documents_type[key] = {"meta": meta}
            else:
                _documents_type[key]["meta"] = meta

            return _documents_type[key]["meta"]
        finally:

            lock.release()


def get_fields(document_class, document_name):

    key = document_name + "|" + document_class.__module__

    if key in _documents_type and "fields" in _documents_type[key]:

        return _documents_type[key]["fields"]

    else:
        lock.acquire()

        try:

            meta = get_meta(document_class, document_name)

            fields = [
                prop
                for prop, value in vars(document_class.__class__).items() if not prop.startswith("_") and
                                                                             type(value) is not staticmethod and
                                                                             not isinstance(value, types.FunctionType)
            ]

            if key not in _documents_type:
                _documents_type[key] = {"fields": []}
            else:
                _documents_type[key]["fields"] = []

            for field in fields:
                _type = type(getattr(document_class, field))
                if _type is list:
                    if field in meta:
                        _type = {
                            "list_type": meta[field]['type']
                        }
                    else:
                        raise TypeListNotFound("Not found child type from {}".format(field))
                elif field in meta:
                    _type = meta[field]['type']
                _documents_type[key]["fields"].append({
                    "name": field,
                    "type": _type
                })

            return _documents_type[key]["fields"]

        finally:

            lock.release()
