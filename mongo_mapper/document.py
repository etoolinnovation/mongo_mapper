from mongo_mapper.core.connection import get_collection
from mongo_mapper.core.id_manager import IdType, get_id
from mongo_mapper.finder import Finder, FinderCollection
from mongo_mapper.writer import Writer

from bson import DBRef
from bson.objectid import ObjectId


class Document:
    def __init__(self):
        self.__meta = self._meta if hasattr(self, "_meta") is not None else {}
        self.__collection_name = self.__meta["collection_name"] if "collection_name" in self.__meta else self.__class__.__name__.lower()
        self.__alias = self.__meta["alias"] if "alias" in self.__meta else "default"
        self.__pk_fields = self.__meta["pk_fields"] if "pk_fields" in self.__meta else ["id"]

        self.__id_type = self.__meta["id_type"] if "id_type" in self.__meta else IdType.ObjectId
        self.__document_class = self

        self.__collection = None
        self.__fields = None

        self.__finder = Finder(self)
        self.__writer = Writer(self)

        self.id = None

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

    def remote_set(self): pass

    def to_dict(self):
        object_dict = {}
        for field in self.get_fields():
            object_dict[field] = getattr(self, field)
        return object_dict

    def get_fields(self):
        if self.__fields is None:
            self.__fields = [prop for prop, value in vars(self.__document_class.__class__).items() if not prop.startswith("_")]

        return self.__fields

    def __set_document__(self, document):
        for field in self.get_fields():
            setattr(self, field, document[field])
        self.id = document['_id']


class DocumentEmbedded:
    def to_dict(self):
        object_dict = {}
        for prop, value in vars(self).items():
            object_dict[prop] = value
        return object_dict


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

    def find(self, args):
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
