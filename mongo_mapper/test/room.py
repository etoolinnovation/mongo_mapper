from mongo_mapper.document import Document


class Room(Document):
    code = ""
    code_dingus = ""
    name = ""

    _meta = {
        "pk_fields": ["code", "code_dingus"],
        "alias": "default"
    }
