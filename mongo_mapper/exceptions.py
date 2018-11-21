###############################
#     Document Exceptions     #
###############################


class TypeListNotFound(Exception):
    def __init__(self, *args, **kwargs):  # real signature unknown
        pass


class DocumentRefNotFoundType(Exception):
    def __init__(self, *args, **kwargs):  # real signature unknown
        pass

###############################
# FinderCollection Exceptions #
###############################


class FindCursorNotFound(Exception):
    def __init__(self, *args, **kwargs):  # real signature unknown
        pass


############################
#    Finder Exceptions     #
############################


class DocumentNotFound(Exception):
    def __init__(self, *args, **kwargs):  # real signature unknown
        pass


############################
#    Writer Exceptions     #
############################


class DuplicatePrimaryKey(Exception):
    def __init__(self, *args, **kwargs):  # real signature unknown
        pass


class MultiInsertErrorIDSpecified(Exception):
    def __init__(self, *args, **kwargs):  # real signature unknown
        pass


class MultiInsertDistinctTypes(Exception):
    def __init__(self, *args, **kwargs):  # real signature unknown
        pass

############################
# Configuration Exceptions #
############################


class DuplicateDefaultAlias(Exception):
    def __init__(self, *args, **kwargs):  # real signature unknown
        pass


class InvalidFormatConfiguration(Exception):
    def __init__(self, *args, **kwargs):  # real signature unknown
        pass


class NotFoundDefaultAliasConfiguration(Exception):
    def __init__(self, *args, **kwargs):  # real signature unknown
        pass


class ConfigurationNotLoaded(Exception):
    def __init__(self, *args, **kwargs):  # real signature unknown
        pass
