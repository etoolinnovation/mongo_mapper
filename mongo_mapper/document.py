from bson import DBRef
from bson.objectid import ObjectId

from mongo_mapper.core.cache import get_collection, get_fields, get_meta
from mongo_mapper.core.id_manager import IdType
from mongo_mapper.finder import Finder, FinderCollection
from mongo_mapper.writer import Writer


def internal_set_document(self, document, document_class, document_name, document_ref_extended=False):
    for field in get_fields(document_class, document_name):
        if field['name'] in document:
            if type(field["type"]) is dict and "list_type" in field["type"]:
                values = []
                for item in document[field["name"]]:
                    if type(field["type"]["list_type"]) is DocumentRef:
                        if type(item) is DBRef:
                            values.append(item)
                        elif type(item) is dict and "id" in item:
                            values.append(DBRef(field["type"]["list_type"].db_ref.collection, item['id']))
                        elif hasattr(item, 'id'):
                            values.append(DBRef(field["type"]["list_type"].db_ref.collection, item.id))
                        else:
                            values.append(DBRef(field["type"]["list_type"].db_ref.collection, item))
                    elif type(field["type"]["list_type"]) is DocumentRefExtended:
                        rec = DocumentRefExtended(
                            field["type"]["list_type"]._DocumentRefExtended__document_class_reference()
                        )
                        rec.__set_document__(item)
                        values.append(rec)
                    elif hasattr(field["type"]["list_type"], "__set_document__"):
                        rec = field["type"]["list_type"].__class__()
                        rec.__set_document__(item)
                        values.append(rec)
                    else:
                        values.append(field["type"]["list_type"](item))
                setattr(self, field["name"], values)
                if document_ref_extended:
                    self._DocumentRefExtended__extended_document[field["name"]] = values

            else:
                setattr(self, field["name"], document[field["name"]])
                if document_ref_extended:
                    self._DocumentRefExtended__extended_document[field["name"]] = document[field["name"]]

def internal_to_dict(self, document_class, document_name):
    object_dict = {}
    for field in get_fields(document_class, document_name):
        value = getattr(self, field["name"])
        if type(value) is list:
            childs = []
            for rec in value:
                if type(field["type"]["list_type"]) is DocumentRef:
                    if type(rec) is DBRef:
                        childs.append(rec)
                    elif type(rec) is dict and "id" in rec:
                        childs.append(DBRef(field["type"]["list_type"].db_ref.collection, rec['id']))
                    elif hasattr(rec, 'id'):
                        childs.append(DBRef(field["type"]["list_type"].db_ref.collection, rec.id))
                    else:
                        childs.append(DBRef(field["type"]["list_type"].db_ref.collection, rec))
                elif "to_dict" in dir(rec):
                    childs.append(rec.to_dict())
                else:
                    childs.append(rec)
            object_dict[field["name"]] = childs
        elif type(field["type"]) is DocumentRef:
            if type(value) is DBRef:
                object_dict[field["name"]] = value
            elif type(value) is dict and "id" in value:
                object_dict[field["name"]] = DBRef(field["type"].db_ref.collection, value['id'])
            elif hasattr(value, 'id'):
                object_dict[field["name"]] = DBRef(field["type"].db_ref.collection, value.id)
            else:
                object_dict[field["name"]] = DBRef(field["type"].db_ref.collection, value)
        else:
            object_dict[field["name"]] = value
    if hasattr(self, 'id'):
        object_dict["id"] = self.id
    return object_dict


class Document:
    def __init__(self, **kwds):
        self.__document_class = self
        self.__document_name = self.__class__.__name__

        self.__meta = get_meta(self.__document_class, self.__document_name)
        self.__collection_name = self.__meta[
            "collection_name"] if "collection_name" in self.__meta else self.__document_name.lower()
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
        if self.id_type == IdType.ObjectId and type(_id) is not ObjectId:
            _id = ObjectId(_id)

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
        return internal_to_dict(self, self.__document_class, self.__document_name)

    def __dict__(self):
        self.to_dict()

    def __set_document__(self, document):
        internal_set_document(self, document, self.__document_class, self.__document_name)
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
        return internal_to_dict(self, self.__document_class, self.__document_name)

    def __set_document__(self, document):
        internal_set_document(self, document, self.__document_class, self.__document_name)
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


class DocumentRefExtended:
    def __init__(self, document, **kwds):
        self.__document_class = self
        self.__document_name = self.__class__.__name__

        self.__document_class_reference = document.__class__
        self.__document_name_reference = document.__class__.__name__

        self.__db_ref = DBRef(collection=document.collection_name, id=document.id)
        self.__finder = Finder(document)

        self.__document_reference = None

        self.__extended_document = {}

        if kwds is not None and kwds:
            self.__set_document__(kwds)

    @property
    def db_ref(self):
        return self.__db_ref

    @property
    def extended_document(self):
        return self.__extended_document

    @extended_document.setter
    def extended_document(self, value):
        self.__extended_document = value

    def __load_reference(self):
        if self.__document_reference is None:
            self.__document_reference = self.__finder.find_by_id(self.__db_ref.id)

    def __getitem__(self, key):
        self.__load_reference()
        if key in self.__extended_document:
            return self.__extended_document[key]
        elif key in self.__document_reference:
            return self.__document_reference[key]
        else:
            return None

    def __setitem__(self, key, value):
        self.__extended_document[key] = value

    def __set_document__(self, document):
        internal_set_document(self, document, self.__document_class_reference, self.__document_name_reference, document_ref_extended=True)
        if "db_ref" in document:
            self.__db_ref = document["db_ref"]

    def to_dict(self):
        object_dict = {"db_ref": self.__db_ref}
        internal_fields = dir(self)
        for field in get_fields(self.__document_class_reference, self.__document_name_reference):
            if field["name"] in self.__extended_document or field["name"] in internal_fields:
                if field["name"] in self.__extended_document:
                    value = self.__extended_document[field["name"]]
                else:
                    value = getattr(self, field["name"])
                if type(value) is list:
                    childs = []
                    for rec in value:
                        if type(field["type"]["list_type"]) is DocumentRef:
                            if type(rec) is DBRef:
                                childs.append(rec)
                            elif type(rec) is dict and "id" in rec:
                                childs.append(DBRef(field["type"]["list_type"].db_ref.collection, rec['id']))
                            elif hasattr(rec, 'id'):
                                childs.append(DBRef(field["type"]["list_type"].db_ref.collection, rec.id))
                            else:
                                childs.append(DBRef(field["type"]["list_type"].db_ref.collection, rec))
                        elif "to_dict" in dir(rec):
                            childs.append(rec.to_dict())
                        else:
                            childs.append(rec)
                    object_dict[field["name"]] = childs
                else:
                    object_dict[field["name"]] = value
        return object_dict


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

    def find(self, args=None, project=None):
        if args is None:
            args = {}
        self.__finder_collection.find(args, project)
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

    def distinct(self, field_name):
        self.__finder_collection.distinct(field_name)
        return self

    def count(self, args):
        return self.__finder_collection.count(args)

    def to_list(self):
        return self.__finder_collection.to_list()

    @property
    def total(self):
        return self.__finder_collection.total()

    def next(self):
        return self.__next__()

    def __next__(self):
        return self.__finder_collection.next()

    def __iter__(self):
        return self
