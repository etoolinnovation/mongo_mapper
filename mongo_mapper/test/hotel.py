from mongo_mapper.document import Document, DocumentCollection, DocumentEmbedded, IdType


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


class Hotel(Document):
    code = ""
    sub_code = ""
    extras = []
    rooms = []

    _meta = {
        "pk_fields": ["code", "sub_code"],
        "alias": "default",
        "id_type": IdType.Incremental
    }


class RoomCol(DocumentCollection):
    # TODO: revisar forma molona de hacerlo
    def __init__(self):
        super().__init__(Room())

    def find_by_name(self, name):
        self.find({"name": {"$regex": ".*{}.*".format(name)}})
