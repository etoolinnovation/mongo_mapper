from mongo_mapper.exceptions import DocumentNotFound, FindCursorNotFound
from mongo_mapper.core.cache import get_fields


class Finder:
    def __init__(self, document):
        self.__document = document

    def find_by_id(self, _id):

        doc = self.__document.collection.find({'_id': _id}).limit(1)
        try:
            doc = doc[0]
            return doc
        except IndexError:
            raise DocumentNotFound("{} not found".format(self.__document.collection_name))

    def find_by_primary_key(self, *kwargs):

        args = {}
        for idx, pk in enumerate(self.__document.pk_fields):
            args[pk] = kwargs[idx]
        doc = self.__document.collection.find(args).limit(1)
        try:
            doc = doc[0]
            return doc
        except IndexError:
            raise DocumentNotFound("{} not found".format(self.__document.collection_name))

    def find_id_by_key(self, *kwargs):

        args = {}
        for idx, pk in enumerate(self.__document.pk_fields):
            args[pk] = kwargs[idx]
        doc = self.__document.collection.find(args, {'_id': 1}).limit(1)
        try:
            doc = doc[0]['_id']
            return doc
        except IndexError:
            raise DocumentNotFound("{} not found".format(self.__document.collection_name))


class FinderCollection:
    def __init__(self, document_collection):
        self.__document_collection = document_collection
        self.__cursor = None

    def find(self, args, project=None):
        self.__cursor = self.__document_collection.collection.find(filter=args, projection=project)
        return self

    def limit(self, limit):
        if self.__cursor is None:
            raise FindCursorNotFound("Find cursor not found")
        elif limit is not None:
            self.__cursor = self.__cursor.limit(limit)
        return self

    def skip(self, skip):
        if self.__cursor is None:
            raise FindCursorNotFound("Find cursor not found")
        elif skip is not None:
            self.__cursor = self.__cursor.skip(skip)
        return self

    def sort(self, sort):
        if self.__cursor is None:
            raise FindCursorNotFound("Find cursor not found")
        elif sort is not None:
            self.__cursor = self.__cursor.sort(sort)
        return self

    def count(self, args):
        return self.__document_collection.collection.count(args)

    def total(self):
        return self.__document_collection.collection.count()

    def next(self):
        return self.__next__()

    def __next__(self):
        if self.__cursor.alive:
            rec = self.__cursor.next()
            if rec is None:
                raise StopIteration

            document = self.__document_collection.document.__class__()
            document_class = self.__document_collection.document
            document_name = document_class.__class__.__name__

            for field in get_fields(document_class, document_name):
                if field['name'] in rec:
                    setattr(document, field['name'], rec[field['name']])
            document.id = rec["_id"]
            return document

    def to_list(self):
        collection = []
        for rec in self.__cursor:
            collection.append(rec)
        return collection
