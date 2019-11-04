from mongo_mapper.exceptions import DocumentNotFound, FindCursorNotFound
from mongo_mapper.core.cache import get_fields
from datetime import date, datetime
from bson.regex import Regex
import re
import pytz


def __parse_value_arg__(arg):
    if type(arg) is date:
        return datetime(year=arg.year, month=arg.month, day=arg.day, tzinfo=pytz.utc)
    else:
        return arg


def __parse_values_args__(args):
    new_args = {}
    for key in args:
        if type(args[key]) is dict:
            new_args[key] = __parse_values_args__(args[key])
        elif type(args[key]) is list:
            new_array = []
            for _arg in args[key]:
                if type(_arg) is dict or type(_arg) is list:
                    new_array.append(__parse_values_args__(_arg))
                else:
                    new_array.append(__parse_value_arg__(_arg))

            new_args[key] = new_array
        else:
            new_args[key] = __parse_value_arg__(args[key])
    return new_args


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
            if pk == "id":
                args["_id"] = kwargs[idx]
            elif pk == 'company_key':
                company_key_is_list = type(kwargs[idx]) is list
                if company_key_is_list:
                    args[pk] = {'$in': kwargs[idx]}
                else:
                    args[pk] = kwargs[idx]
            else:
                is_case_insensitive_pk = 'insensitive_pk_fields' in self.__document._meta and pk in self.__document._meta['insensitive_pk_fields']
                if not is_case_insensitive_pk:
                    args[pk] = kwargs[idx]
                else:
                    regex = Regex.from_native(re.compile("^" + kwargs[idx] + "$", re.IGNORECASE))
                    query_insensitive = {"$regex": regex}
                    args[pk] = query_insensitive
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
        mapped_args = __parse_values_args__(args)
        self.__cursor = self.__document_collection.collection.find(filter=mapped_args, projection=project)
        return self

    def aggregate(self, pipeline, collation={}):
        self.__cursor = self.__document_collection.collection.aggregate(pipeline, collation=collation)
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

    def distinct(self, field_name):
        if self.__cursor is None:
            raise FindCursorNotFound("Find cursor not found")
        elif field_name is not None:
            self.__cursor = self.__cursor.distinct(field_name)
        return self

    def count(self, args):
        return self.__document_collection.collection.count(args)

    def total(self):
        return self.__document_collection.collection.count()

    def next(self):
        return self.__next__()

    def __next__(self):
        if self.__cursor is not None and self.__cursor.alive:
            rec = self.__cursor.next()
            if rec is None:
                raise StopIteration

            document = self.__document_collection.document.__class__()
            document.__set_document__(rec)
            return document
        else:
            raise StopIteration

    def __getitem__(self, index):
        if self.__cursor.alive:
            rec = self.__cursor[index]

            document = self.__document_collection.document.__class__()
            document.__set_document__(rec)
            return document

    def __len__(self):
        if self.__cursor.alive:
            return self.__cursor.count()

    def to_list(self):
        collection = []
        for rec in self.__cursor:
            collection.append(rec)
        return collection
