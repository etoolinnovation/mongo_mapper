############################
#    Finder Exceptions     #
############################


class DocumentNotFound(Exception):
    def __init__(self, *args, **kwargs):    # real signature unknown
        pass


############################
#    Writer Exceptions     #
############################


class DuplicatePrimaryKey(Exception):
    def __init__(self, *args, **kwargs):    # real signature unknown
        pass

############################
# Configuration Exceptions #
############################


class DuplicateDefaultAlias(Exception):
    def __init__(self, *args, **kwargs):    # real signature unknown
        pass


class InvalidFormatConfiguration(Exception):
    def __init__(self, *args, **kwargs):    # real signature unknown
        pass


class NotFoundDefaultAliasConfiguration(Exception):
    def __init__(self, *args, **kwargs):    # real signature unknown
        pass


class ConfigurationNotLoaded(Exception):
    def __init__(self, *args, **kwargs):    # real signature unknown
        pass
