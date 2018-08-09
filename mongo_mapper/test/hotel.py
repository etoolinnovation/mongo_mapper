from mongo_mapper.document import Document, DocumentEmbedded, IdType


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
