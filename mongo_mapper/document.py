from mongo_mapper.core.connection import get_collection
from mongo_mapper.core.id_manager import IdType
from mongo_mapper.finder import Finder
from mongo_mapper.writer import Writer


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

        self.__finder = Finder(self)
        self.__writer = Writer(self)

    def find_by_id(self, _id):
        doc = self.__finder.find_by_id(_id)
        self.__set_document__(doc)

    def find_by_pk(self, *kwargs):
        doc = self.__finder.find_id_by_key(kwargs)
        self.__set_document__(doc)

    def save(self):
        self.__writer.save()

    def delete(self):
        return self.__writer.delete()

    def to_dict(self):
        object_dict = {}
        for field in self.get_fields():
            object_dict[field] = getattr(self, field)
        return object_dict

    def remote_set(self): pass

    def __set_document__(self, document):
        for field in self.get_fields():
            setattr(self, field, document[field])
        self.id = document['_id']

    def get_fields(self):
        if self.__fields is None:
            self.__fields = [prop for prop, value in vars(self.__document_class.__class__).items() if not prop.startswith("_")]

        return self.__fields

    def get_collection(self):

        if self.__collection is None:
            self.__collection = get_collection(self.__alias, self.__collection_name)

        return self.__collection



class DocumentCollection:
    def find(self): pass

    def count(self): pass

    def to_list(self): pass

    def total(self): pass