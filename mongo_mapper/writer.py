from pymongo import ReturnDocument

from mongo_mapper.core.id_manager import get_id
from mongo_mapper.exceptions import DocumentNotFound, DuplicatePrimaryKey


class Writer:
    def __init__(self, document):
        self.__document = document

    def save(self):

        if self.__document.id is None:
            check_pk = False
            kwargs = [getattr(self.__document, field) for field in self.__document.pk_fields]
            try:
                self.__document.find_by_pk(*kwargs)
            except DocumentNotFound:
                check_pk = True
            if check_pk:
                _id = get_id(self.__document.id_type, self.__document.collection_name)
                doc = self.__document.to_dict()
                doc["_id"] = _id
                self.__document.collection.insert_one(doc)
                self.__document.__set_document__(doc)
            else:
                raise DuplicatePrimaryKey("Duplicate primary keys: {}".format(self.__document.pk_fields))

        else:
            doc = self.__document.to_dict()
            result = self.__document.collection.find_one_and_replace(filter={'_id': self.__document.id},
                                                                     replacement=doc,
                                                                     upsert=True,
                                                                     return_document=ReturnDocument.AFTER)
            self.__document.__set_document__(result)

    def delete(self):
        result = self.__document.collection.delete_one({"_id": self.__document.id})
        return result.acknowledged
