import pymongo
from pymongo import GEO2D, GEOSPHERE
from mongo_mapper.core.cache import get_meta
from mongo_mapper.indexes import MongoIndex, MongoTTLIndex, Mongo2dIndex, Mongo2dSpehreIndex, DEFAULTS_MONGO_2D_INDEX


def create_index(document, rebuild):
    list_index = document.collection.list_indexes()
    __create_index_pk(document.collection, document.pk_fields, rebuild, list_index)

    meta = get_meta(document, document.__class__.__name__)
    if "indexes" in meta:
        for _index in meta["indexes"]:
            if type(_index) is MongoIndex:
                __create_index_ix_or_u(document.collection, _index, rebuild, list_index)
            elif type(_index) is MongoTTLIndex:
                __create_index_ttl(document.collection, _index, rebuild, list_index)
            elif type(_index) is Mongo2dIndex:
                __create_index_2d(document.collection, _index, rebuild, list_index)
            elif type(_index) is Mongo2dSpehreIndex:
                __create_index_2dsphere(document.collection, _index, rebuild, list_index)


def __create_index_pk(collection, primary_keys, rebuild, list_index):
    pk_index = []
    name_index = "pk_"
    for i, primary_key in enumerate(primary_keys):
        pk_index.append((primary_key, pymongo.ASCENDING))
        name_index += primary_key
        if i < len(primary_keys) - 1:
            name_index += "_"

    flag_create_index = rebuild
    if rebuild and name_index in list_index:
        collection.drop_index(name_index)

    if flag_create_index is False:
        if name_index not in list_index:
            flag_create_index = True

    if flag_create_index is True:
        collection.create_index(pk_index, unique=True, name=name_index)


def __create_index_ix_or_u(collection, mongo_index, rebuild, list_index):
    ix_index = []
    name_index = "ix_" if mongo_index.unique is False else "u_"
    for i, field in enumerate(mongo_index.fields):
        ix_index.append((field, pymongo.ASCENDING))
        name_index += field
        if i < len(mongo_index.fields) - 1:
            name_index += "_"

    flag_create_index = rebuild
    if rebuild and name_index in list_index:
        collection.drop_index(name_index)

    if flag_create_index is False:
        if name_index not in list_index:
            flag_create_index = True

    if flag_create_index is True:
        collection.create_index(ix_index, name=name_index, unique=mongo_index.unique)


def __create_index_ttl(collection, mongo_index, rebuild, list_index):
    ttl_index = mongo_index.field_date
    name_index = "ttl_{}".format(mongo_index.field_date)

    flag_create_index = rebuild
    if rebuild and name_index in list_index:
        collection.drop_index(name_index)

    if flag_create_index is False:
        if name_index not in list_index:
            flag_create_index = True

    if flag_create_index is True:
        collection.create_index(ttl_index, name=name_index, expireAfterSeconds=mongo_index.expire_after_seconds)


def __create_index_2d(collection, mongo_index, rebuild, list_index):
    twod_index = mongo_index.field
    name_index = "2d_{}".format(mongo_index.field)

    flag_create_index = rebuild
    if rebuild and name_index in list_index:
        collection.drop_index(name_index)

    if flag_create_index is False:
        if name_index not in list_index:
            flag_create_index = True

    if flag_create_index is True:
        if DEFAULTS_MONGO_2D_INDEX["MIN"] != mongo_index.min or DEFAULTS_MONGO_2D_INDEX["MAX"] != mongo_index.max:
            collection.create_index((twod_index, GEO2D), name=name_index, min=mongo_index.min, max=mongo_index.max)
        else:
            collection.create_index((twod_index, GEO2D), name=name_index)


def __create_index_2dsphere(collection, mongo_index, rebuild, list_index):
    twodsphere_index = mongo_index.field
    name_index = "2dsphere_{}".format(mongo_index.field)

    flag_create_index = rebuild
    if rebuild and name_index in list_index:
        collection.drop_index(name_index)

    if flag_create_index is False:
        if name_index not in list_index:
            flag_create_index = True

    if flag_create_index is True:
        collection.create_index((twodsphere_index, GEOSPHERE), name=name_index)



