from mongo_mapper.core.connection import get_collection


class MongoMapper:
    def __init__(self, alias="", object_name="", id_type=""):
        if alias == "":
            alias = "default"
        if object_name == "":
            object_name = self.__class__.__name__.lower()
        self.__alias = alias
        self.__object_name = object_name
        self.__id_type = None

        self.__collection = None
        # self.__pk_fields

    def __check_collection(self):
        self.__collection = get_collection(self.__alias, self.__object_name)

    def find_by_pk(self, *kwargs):
        self.__check_collection()
        # self.__collection.find()

    def save(self):
        self.__check_collection()
        self.__collection.save(self)

    def delete(self): pass

    def remote_set(self): pass


class MongoMapperCollection:
    def find(self): pass

    def count(self): pass

    def to_list(self): pass

    def total(self): pass