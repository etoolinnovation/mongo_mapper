from pymongo import ReturnDocument

from mongo_mapper.core.id_manager import IdType, get_id
from mongo_mapper.exceptions import DocumentNotFound, DuplicatePrimaryKey


class Writer:
    def __init__(self, document):
        self.__document = document

    def save(self):

        if self.__document.id is None:
            check_pk = False
            kwargs = [getattr(self.__document, field) for field in self.__document.__pk_fields]
            try:
                self.__document.find_by_pk(tuple(kwargs))
            except DocumentNotFound:
                check_pk = True
            if check_pk:
                _id = get_id(self.__document.__id_type, self.__document.__collection_name)
                doc = self.__document.to_dict()
                doc["_id"] = _id
                result = self.__document.get_collection().insert_one(doc)
                self.__document.__set_document__(doc)
            else:
                raise DuplicatePrimaryKey("Duplicate primary keys: {}".format(self.__document.__pk_fields))

        else:
            doc = self.__document.to_dict()
            result = self.__document.get_collection().find_one_and_replace(filter={'_id': doc['_id']}, replacement=doc, upsert=True, return_document=ReturnDocument.AFTER)
            self.__document.__set_document__(result)

    def delete(self):
        result = self.__document.get_collection.delete_one({"_id": self.__document.id})
        return result.acknowledged
