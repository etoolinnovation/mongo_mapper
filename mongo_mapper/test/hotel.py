from mongo_mapper.document import Document, DocumentCollection, DocumentEmbedded, IdType, DocumentRef, DocumentRefExtended


class Room(Document):
    code = ""
    sub_code = ""
    name = ""

    _meta = {
        "pk_fields": ["code", "sub_code"],
        "alias": "default",
        "id_type": IdType.Incremental
    }


class Extra(DocumentEmbedded):
    code = ""
    sub_code = ""
    name = ""

    _meta = {
        "id_type": IdType.ObjectId
    }


class Hotel(Document):
    code = ""
    sub_code = ""
    extras = []
    rooms = []
    rooms_extended = []

    _meta = {
        "pk_fields": ["code", "sub_code"],
        "alias": "default",
        "id_type": IdType.Incremental,
        "rooms": {
            "type": DocumentRef(Room())
        },
        "extras": {
            "type": Extra()
        },
        "rooms_extended": {
            "type": DocumentRefExtended(Room())
        }
    }


class RoomCol(DocumentCollection):
    # TODO: revisar forma molona de hacerlo
    def __init__(self):
        super().__init__(Room())

    def find_by_name(self, name):
        self.find({"name": {"$regex": ".*{}.*".format(name)}})


class RoomBO:
    def __init__(self, code="", sub_code="", name=""):
        self.__code = code
        self.__sub_code = sub_code
        self.__name = name
        self.__data = Room()

    @property
    def code(self):
        return self.__code

    @code.setter
    def code(self, value):
        self.__code = value

    @property
    def sub_code(self):
        return self.__sub_code

    @sub_code.setter
    def sub_code(self, value):
        self.__sub_code = value

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    def set_data(self, data):
        self.__data = data

    def delete(self):
        self.__data.delete()


class RoomBOCollection:
    def __init__(self):
        self.__finder = RoomCol()

    def fill_by_name(self, name):
        self.__finder.find_by_name(name)

    def __next__(self):
        rec = self.__finder.next()
        if rec is None:
            raise StopIteration
        room = RoomBO(rec.code, rec.sub_code, rec.name)
        room.set_data(rec)
        return room

    def __iter__(self):
        return self

    def __getitem__(self, index):
        return self.__finder[index]


