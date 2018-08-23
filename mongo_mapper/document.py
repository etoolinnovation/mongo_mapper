from bson import DBRef

from mongo_mapper.core.cache import get_collection, get_fields, get_meta
from mongo_mapper.core.id_manager import IdType
from mongo_mapper.finder import Finder, FinderCollection
from mongo_mapper.writer import Writer
from mongo_mapper.exceptions import TypeListNotFound, DocumentRefNotFoundType


class Document:
    def __init__(self, **kwds):
        self.__document_class = self
        self.__document_name = self.__class__.__name__

        self.__meta = get_meta(self.__document_class, self.__document_name)
        self.__collection_name = self.__meta["collection_name"] if "collection_name" in self.__meta else self.__document_name.lower()
        self.__alias = self.__meta["alias"] if "alias" in self.__meta else "default"
        self.__pk_fields = self.__meta["pk_fields"] if "pk_fields" in self.__meta else ["id"]

        self.__id_type = self.__meta["id_type"] if "id_type" in self.__meta else IdType.ObjectId

        self.__collection = None

        self.__finder = Finder(self)
        self.__writer = Writer(self)

        self.id = None
        if kwds is not None and kwds:
            self.__set_document__(kwds)

    @property
    def collection_name(self):
        return self.__collection_name

    @property
    def pk_fields(self):
        return self.__pk_fields

    @property
    def id_type(self):
        return self.__id_type

    @property
    def collection(self):
        if self.__collection is None:
            self.__collection = get_collection(self.__alias, self.collection_name)

        return self.__collection

    def find_by_id(self, _id):
        doc = self.__finder.find_by_id(_id)
        self.__set_document__(doc)

    def find_by_pk(self, *kwargs):
        doc = self.__finder.find_by_primary_key(*kwargs)
        self.__set_document__(doc)

    def save(self):
        self.__writer.save()

    def delete(self):
        return self.__writer.delete()

    def remote_set(self):
        pass

    def to_dict(self):
        object_dict = {}
        for field in get_fields(self.__document_class, self.__document_name):
            value = getattr(self, field["name"])
            if type(value) is list:
                childs = []
                for rec in value:
                    if "to_dict" in dir(rec):
                        childs.append(rec.to_dict())
                    else:
                        childs.append(rec)
                object_dict[field["name"]] = childs
            else:
                object_dict[field["name"]] = value
        object_dict["id"] = self.id
        return object_dict

    def __dict__(self):
        self.to_dict()

    def __set_document__(self, document):
        for field in get_fields(self.__document_class, self.__document_name):
            if field['name'] in document:
                if type(field["type"]) is dict and "list_type" in field["type"]:
                    values = []
                    for item in document[field["name"]]:
                        if type(field["type"]["list_type"]) is DocumentRef:
                            values.append(DBRef(field["type"]["list_type"].db_ref.collection, item))
                        elif hasattr(field["type"]["list_type"], "__set_document__"):
                            rec = field["type"]["list_type"].__class__()
                            rec.__set_document__(item)
                            values.append(rec)
                        else:
                            values.append(field["type"]["list_type"](item))
                    setattr(self, field["name"], values)
                else:
                    setattr(self, field["name"], document[field["name"]])
        if "_id" in document:
            self.id = document['_id']

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        setattr(self, key, value)


class DocumentEmbedded:
    def __init__(self, **kwds):
        self.__document_class = self
        self.__document_name = self.__class__.__name__

        self.__meta = get_meta(self.__document_class, self.__document_name)

        if kwds is not None and kwds:
            self.__set_document__(kwds)

    def to_dict(self):
        object_dict = {}
        for field in get_fields(self.__document_class, self.__document_name):
            value = getattr(self, field["name"])
            if type(value) is list:
                childs = []
                for rec in value:
                    if "to_dict" in dir(rec):
                        childs.append(rec.to_dict())
                    else:
                        childs.append(rec)
                object_dict[field["name"]] = childs
            else:
                object_dict[field["name"]] = value
        return object_dict

    def __set_document__(self, document):
        for field in get_fields(self.__document_class, self.__document_name):
            if field['name'] in document:
                if type(field["type"]) is dict and "list_type" in field["type"]:
                    values = []
                    for item in document[field["name"]]:
                        if type(field["type"]["list_type"]) is DocumentRef:
                            values.append(DBRef(field["type"]["list_type"].db_ref.collection, item))
                        elif hasattr(field["type"]["list_type"], "__set_document__"):
                            rec = field["type"]["list_type"].__class__()
                            rec.__set_document__(item)
                            values.append(rec)
                        else:
                            values.append(field["type"]["list_type"](item))
                    setattr(self, field["name"], values)
                else:
                    setattr(self, field["name"], document[field["name"]])
        if "_id" in document:
            self.id = document['_id']

    def __dict__(self):
        self.to_dict()

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        setattr(self, key, value)


class DocumentRef:
    def __init__(self, document):
        self.__db_ref = DBRef(collection=document.collection_name, id=document.id)

    @property
    def db_ref(self):
        return self.__db_ref


class DocumentCollection:
    def __init__(self, document):
        self.__document = document
        self.__finder_collection = FinderCollection(self)

    @property
    def collection(self):
        return self.__document.collection

    @property
    def document(self):
        return self.__document

    def find(self, args=None):
        if args is None:
            args = {}
        self.__finder_collection.find(args)
        return self

    def skip(self, skip):
        self.__finder_collection.skip(skip)
        return self

    def limit(self, limit):
        self.__finder_collection.limit(limit)
        return self

    def sort(self, sort):
        self.__finder_collection.sort(sort)
        return self

    def count(self, args):
        return self.__finder_collection.count(args)

    def to_list(self):
        return self.__finder_collection.to_list()

    @property
    def total(self):
        return self.__finder_collection.total()

    def __iter__(self):
        for rec in self.__finder_collection:
            yield rec
