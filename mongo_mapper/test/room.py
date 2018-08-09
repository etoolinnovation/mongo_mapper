from mongo_mapper.document import Document, IdType


class Room(Document):
    code = ""
    code_dingus = ""
    name = ""

    _meta = {
        "pk_fields": ["code", "code_dingus"],
        "alias": "default",
        "id_type": IdType.Incremental
    }
