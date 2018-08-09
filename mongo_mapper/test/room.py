from mongo_mapper import MongoMapper


class Room(MongoMapper):
    code = ""
    code_dingus = ""
    name = ""

    _meta = {
        "pk_fields": ["code", "code_dingus"],
        "alias": "default"
    }
