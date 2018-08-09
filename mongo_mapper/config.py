from mongo_mapper.exceptions import DuplicateDefaultAlias, InvalidFormatConfiguration, \
    NotFoundDefaultAliasConfiguration, ConfigurationNotLoaded

__MONGODB_SETTINGS = None


@property
def MONGODB_SETTINGS():
    global __MONGODB_SETTINGS
    if __MONGODB_SETTINGS is None:
        raise ConfigurationNotLoaded('MONGODB SETTINGS not loaded')
    else:
        return __MONGODB_SETTINGS


class __Instance:
    def __init__(self):
        self.__MONGODB_SETTINGS = None
        self.__check_default = False
    
    def create_config(self, configuraton_obj):
        if type(configuraton_obj) is list:
            self.__MONGODB_SETTINGS = []
            for conf in configuraton_obj:
                self.append_config(conf)
            if not self.__check_default:
                raise NotFoundDefaultAliasConfiguration("Not found default ALIAS")
        elif type(configuraton_obj) is dict:
            self.__MONGODB_SETTINGS = []
            self.append_config(configuraton_obj)
            if not self.__check_default:
                raise NotFoundDefaultAliasConfiguration("Not found default ALIAS")
        elif type(configuraton_obj) is str:
            # load module configuration an search MONGODB_SETTINGS section
            pass
        return self.__MONGODB_SETTINGS
        
    def append_config(self, conf):
        if type(conf) is dict:
            if "ALIAS" in conf and "URL" in conf and "DB_NAME" in conf:
                self.__MONGODB_SETTINGS.append(conf)
                if conf["ALIAS"] == "default":
                    if self.__check_default:
                        raise DuplicateDefaultAlias("Duplicate default ALIAS")
                    self.__check_default = True
            else:
                raise InvalidFormatConfiguration("Invalid format configuration")


def load_config(configuraton_obj):
    global MONGODB_SETTINGS
    MONGODB_SETTINGS = __Instance().create_config(configuraton_obj)

    


