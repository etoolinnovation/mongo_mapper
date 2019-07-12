from mongo_mapper.exceptions import NotFoundFieldsMongoIndex, TypeErrorFieldsMongoIndex, FieldNotSpecifiedMongoIndex, \
    InvalidExpirationValueMongoIndex


DEFAULTS_MONGO_2D_INDEX = {
    "MIN": -180,
    "MAX": 180,
    # "BITS": 26
}


class MongoIndex:
    def __init__(self, fields=None, unique=False):
        if fields is None:
            raise NotFoundFieldsMongoIndex()
        if type(fields) is not list:
            raise TypeErrorFieldsMongoIndex("Fields has to be array")
        self.__fields = fields
        self.__unique = unique

    @property
    def fields(self):
        return self.__fields

    @property
    def unique(self):
        return self.__unique


class MongoTTLIndex:
    def __init__(self, field_date="", expire_after_seconds=0):
        if field_date == "":
            raise FieldNotSpecifiedMongoIndex("Field not specified")
        if expire_after_seconds == 0 or expire_after_seconds < 0:
            raise InvalidExpirationValueMongoIndex("the expiration value must be greater than 0")

        self.__field_date = field_date
        self.__expire_after_seconds = expire_after_seconds

    @property
    def field_date(self):
        return self.__field_date

    @property
    def expire_after_seconds(self):
        return self.__expire_after_seconds


class Mongo2dIndex:
    def __init__(self, field="", min=DEFAULTS_MONGO_2D_INDEX["MIN"], max=DEFAULTS_MONGO_2D_INDEX["MAX"]):
        if field == "":
            raise FieldNotSpecifiedMongoIndex("Field not specified")

        self.__field = field
        self.__min = min
        self.__max = max

    @property
    def field(self):
        return self.__field

    @property
    def min(self):
        return self.__min

    @property
    def max(self):
        return self.__max


class Mongo2dSpehreIndex:
    def __init__(self, field=""):
        if field == "":
            raise FieldNotSpecifiedMongoIndex("Field not specified")

        self.__field = field

    @property
    def field(self):
        return self.__field