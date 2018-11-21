from pymongo import ReturnDocument

from mongo_mapper.core.id_manager import get_id
from mongo_mapper.exceptions import DocumentNotFound, DuplicatePrimaryKey, MultiInsertErrorIDSpecified, MultiInsertDistinctTypes


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
                if "id" in doc:
                    doc.pop("id", None)
                self.__document.collection.insert_one(doc)
                self.__document.__set_document__(doc)
            else:
                raise DuplicatePrimaryKey("Duplicate primary keys: {}".format(self.__document.pk_fields))

        else:
            self.__document.__set_document__(self.__document.to_dict())
            doc = self.__document.to_dict()
            if "id" in doc:
                doc['_id'] = doc['id']
                doc.pop("id", None)
            result = self.__document.collection.find_one_and_replace(filter={'_id': self.__document.id},
                                                                     replacement=doc,
                                                                     upsert=True,
                                                                     return_document=ReturnDocument.AFTER)
            self.__document.__set_document__(result)

    def delete(self):
        result = self.__document.collection.delete_one({"_id": self.__document.id})
        return result.acknowledged

    @staticmethod
    def multi_insert(documents):
        if len(documents) > 0:
            document = documents[0]
            insert_collection = []

            _ids = get_id(document.id_type, document.collection_name, len(documents))
            for i, doc in enumerate(documents):
                if doc.id is not None:
                    raise MultiInsertErrorIDSpecified
                if type(doc) != type(document):
                    raise MultiInsertDistinctTypes

                _doc = doc.to_dict()
                _doc['_id'] = _ids[i]
                if "id" in _doc:
                    _doc.pop("id", None)

                insert_collection.append(_doc)

            result = document.collection.insert_many(insert_collection)

            if result.acknowledged:
                for i, id in enumerate(result.inserted_ids):
                    documents[i].id = id

        return documents
