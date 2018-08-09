from pymongo import ReturnDocument

from mongo_mapper.core.id_manager import IdType, get_id


class Writer:
    def __init__(self, document):
        self.__document = document

    def save(self):

        if self.__document.id is None:
            #TODO: revisar si ya existe con la PK y si no dar error de duplicado
            _id = get_id(self.__document.__id_type, self.__document.__collection_name)
            doc = self.__document.to_dict()
            doc["_id"] = _id
            result = self.__document.get_collection().insert_one(doc)

        else:
            doc = self.__document.to_dict()
            result = self.__document.get_collection().find_one_and_replace(filter={'_id': doc['_id']}, update={"$inc": {'count': 1}}, upsert=True, return_document=ReturnDocument.AFTER)
            self.__document.__set_document__(result)

    def delete(self):
        result = self.__document.get_collection.delete_one({"_id": self.__document.id})
        return result.acknowledged
