from mongo_mapper.exceptions import DocumentNotFound, FindCursorNotFound


class Finder:
    def __init__(self, document):
        self.__document = document

    def find_by_id(self, _id):

        doc = self.__document.collection.find({'_id': id}).limit(1)
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

    def find(self, args):
        self.__cursor = self.__document_collection.collection.find(args)
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

    def __iter__(self):
        for rec in self.__cursor:
            document = self.__document_collection.document.__class__()
            for field in document.get_fields():
                setattr(document, field, rec[field])
            document.id = rec["_id"]
            yield document

    def to_list(self):
        collection = []
        for rec in self.__cursor:
            collection.append(rec)
        return collection
