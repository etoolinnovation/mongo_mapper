from mongo_mapper import MongoMapper


class Room(MongoMapper):
    def __init__(self):
        super().__init__()
        self.code = ""
        self.name = ""
