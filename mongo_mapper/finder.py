from mongo_mapper.core.connection import get_collection
from mongo_mapper.exceptions import DocumentNotFound


class Finder:
    def __init__(self, document):
        self.__document = document

    def find_by_id(self, _id):

        doc = self.__collection.find({'_id': id}).limit(1)
        try:
            doc = doc[0]
            return doc
        except IndexError:
            raise DocumentNotFound("{} not found".format(self.__document.__collection_name))

    def find_by_primary_key(self, *kwargs):

        args = {}
        for idx, pk in enumerate(self.__document.__pk_fields):
            args[pk] = kwargs[idx]
        doc = self.__collection.find(args).limit(1)
        try:
            doc = doc[0]
            return doc
        except IndexError:
            raise DocumentNotFound("{} not found".format(self.__document.__collection_name))

    def find_id_by_key(self, *kwargs):

        args = {}
        for idx, pk in enumerate(self.__document.__pk_fields):
            args[pk] = kwargs[idx]
        doc = self.__collection.find(args, {'_id': 1}).limit(1)
        try:
            doc = doc[0]['_id']
            return doc
        except IndexError:
            raise DocumentNotFound("{} not found".format(self.__document.__collection_name))

    def __check_collection__(self):

        self.__collection = get_collection(self.__document.__alias, self.__document.__collection_name)

