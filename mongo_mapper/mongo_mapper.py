class MongoMapper:
    def __init__(self):
        self.__alias = ""
        self.__object_name = ""
        self.__id_type = None
        # self.__pk_fields

    def find_by_pk(self, **kwargs): pass

    def save(self): pass

    def delete(self): pass

    def remote_set(self): pass


class MongoMapperCollection:
    def find(self): pass

    def count(self): pass

    def to_list(self): pass

    def total(self): pass

