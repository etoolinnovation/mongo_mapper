from bson.regex import Regex
import re


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
        if isinstance(value, str) and '%' in value:
            return Query.like(field, value)

        if value is None:
            return Query.add_and({field: value}, Query.field_exist(field, False))

        if isinstance(value, str) and value == '':
            return Query.add_and({field: value}, Query.field_exist(field, False))

        if isinstance(value, bool) and not value:
            return Query.add_and({field: value}, Query.field_exist(field, False))

        if isinstance(value, int) and value == 0:
            return Query.add_and({field: value}, Query.field_exist(field, False))

        if isinstance(value, float) and value == 0.0:
            return Query.add_and({field: value}, Query.field_exist(field, False))

        return {field: value}

    @staticmethod
    def ne(field, value):
        return {field: {"$ne": value}}

    @staticmethod
    def gt(field, value):
        if isinstance(value, int) and value < 0:
            return Query.add_and({field: {"$gt": value}}, Query.field_exist(field, False))

        if isinstance(value, float) and value < 0.0:
            return Query.add_and({field: {"$gt": value}}, Query.field_exist(field, False))

        return {field: {"$gt": value}}

    @staticmethod
    def gte(field, value):
        if isinstance(value, int) and value <= 0:
            return Query.add_and({field: {"$gte": value}}, Query.field_exist(field, False))

        if isinstance(value, float) and value <= 0.0:
            return Query.add_and({field: {"$gte": value}}, Query.field_exist(field, False))

        return {field: {"$gte": value}}

    @staticmethod
    def lt(field, value):
        if isinstance(value, int) and value > 0:
            return Query.add_and({field: {"$lt": value}}, Query.field_exist(field, False))

        if isinstance(value, float) and value > 0.0:
            return Query.add_and({field: {"$lt": value}}, Query.field_exist(field, False))

        return {field: {"$lt": value}}

    @staticmethod
    def lte(field, value):
        if isinstance(value, int) and value >= 0:
            return Query.add_and({field: {"$lte": value}}, Query.field_exist(field, False))

        if isinstance(value, float) and value >= 0.0:
            return Query.add_and({field: {"$lte": value}}, Query.field_exist(field, False))

        return {field: {"$lte": value}}

    @staticmethod
    def field_exist(field, exist):
        return {field: {'$exists': exist}}

    @staticmethod
    def near(field, latitude, longitude, max_distance_in_meters):
        query = {field: {'$near': {'$geometry': {'type': 'Point', 'coordinates': [longitude, latitude]}, '$maxDistance': max_distance_in_meters}}}
        return query

    @staticmethod
    def geo_intersects(field, latitude, longitude):
        query = {field: {'$geoIntersects': {'$geometry': {'type': 'Point', 'coordinates': [longitude, latitude]}}}}
        return query

    @staticmethod
    def like(field, value):
        if value.startswith('%') and value.endswith('%'):
            value = re.compile('.*' + value.replace('%', '') + '.*', re.IGNORECASE)
        elif value.startswith('%'):
            value = re.compile(value.replace('%', '') + '$', re.IGNORECASE)
        elif value.endswith('%'):
            value = re.compile('^' + value.replace('%', ''), re.IGNORECASE)

        return {field: {'$regex': Regex.from_native(value)}}
