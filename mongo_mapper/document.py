from mongo_mapper.core.connection import get_collection
from mongo_mapper.core.id_manager import IdType, get_id
from mongo_mapper.exceptions import DocumentNotFound

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

        self.id = None

    @property
    def collection_name(self):
        return self.__collection_name

    def find_by_pk(self, *kwargs):
        self.__check_collection__()
        self.__check_fields__()
        args = {}
        for idx, pk in enumerate(self.__pk_fields):
            args[pk] = kwargs[idx]
        doc = self.__collection.find(args).limit(1)
        try:
            doc = doc[0]
        except IndexError:
            raise DocumentNotFound("{} not found".format(self.__collection_name))
        self.__set_document__(doc)

    def save(self):
        self.__check_collection__()
        _id = get_id(self.__id_type, self.__collection_name)
        doc = self.to_dict()
        doc["_id"] = _id
        self.__collection.save(doc)
        self.id = _id

    def to_dict(self):
        self.__check_fields__()
        object_dict = {}
        for field in self.__fields:
            object_dict[field] = getattr(self, field)
        return object_dict

    def delete(self):
        self.__check_fields__()
        self.__check_collection__()
        result = self.__collection.delete_one({"_id": self.id})
        return result.acknowledged

    def remote_set(self): pass

    def __check_fields__(self):
        if self.__fields is None:
            self.__fields = [prop for prop, value in vars(self._Document__document_class.__class__).items() if not prop.startswith("_")]

    def __check_collection__(self):
        self.__collection = get_collection(self.__alias, self.__collection_name)

    def __set_document__(self, document):
        for field in self.__fields:
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
    def find(self): pass

    def count(self): pass

    def to_list(self): pass

    def total(self): pass