class Query:

    @staticmethod
    def add_and(*query_list):
        q = list(query_list)
        return {'$and': q}

    @staticmethod
    def add_or(*query_list):
        q = list(query_list)
        return {'$or': q}

    @staticmethod
    def eq(field, value):
        return {field: value}

    @staticmethod
    def ne(field, value):
        return {field: {"$ne": value}}

    @staticmethod
    def gt(field, value):
        return {field: {"$gt": value}}

    @staticmethod
    def gte(field, value):
        return {field: {"$gte": value}}

    @staticmethod
    def lt(field, value):
        return {field: {"$lt": value}}

    @staticmethod
    def lte(field, value):
        return {field: {"$lte": value}}

    @staticmethod
    def regex(): pass
