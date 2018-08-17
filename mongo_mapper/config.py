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

    def create_config(self, configuraton_obj, OLD_MONGODB_SETTINGS=None):
        if OLD_MONGODB_SETTINGS is None:
            self.__MONGODB_SETTINGS = []
        else:
            self.__MONGODB_SETTINGS = OLD_MONGODB_SETTINGS
        if type(configuraton_obj) is list:
            for conf in configuraton_obj:
                self.append_config_line(conf)
            if not self.__check_default:
                raise NotFoundDefaultAliasConfiguration("Not found default ALIAS")
        elif type(configuraton_obj) is dict:
            self.append_config_line(configuraton_obj)
            if not self.__check_default:
                raise NotFoundDefaultAliasConfiguration("Not found default ALIAS")
        elif type(configuraton_obj) is str:
            # load module configuration an search MONGODB_SETTINGS section
            pass
        return self.__MONGODB_SETTINGS

    def append_config_line(self, conf):
        if type(conf) is dict:
            if "ALIAS" in conf and "URL" in conf and "DB_NAME" in conf:
                if conf["ALIAS"] == "default":
                    if self.__check_default:
                        raise DuplicateDefaultAlias("Duplicate default ALIAS")
                    self.__check_default = True
                setting = [s for s in self.__MONGODB_SETTINGS if s['ALIAS'] == conf["ALIAS"]]
                if len(setting) > 0:  # update setting
                    for s in self.__MONGODB_SETTINGS:
                        if s['ALIAS'] == conf["ALIAS"]:
                            s['URL'] = conf['URL']
                            s['DB_NAME'] = conf['DB_NAME']
                            # s['UPDATE_CONNECTION'] = True
                else:  # add new setting
                    self.__MONGODB_SETTINGS.append(conf)
            else:
                raise InvalidFormatConfiguration("Invalid format configuration")


def load_config(configuraton_obj):
    global MONGODB_SETTINGS
    MONGODB_SETTINGS = __Instance().create_config(configuraton_obj)


def add_config(configuraton_obj):
    global MONGODB_SETTINGS
    if MONGODB_SETTINGS is None:
        load_config(configuraton_obj)
    else:
        MONGODB_SETTINGS = __Instance().create_config(configuraton_obj, MONGODB_SETTINGS)
