from mongo_mapper.core.id_manager import IdType, get_id
from mongo_mapper import config

config.load_config([
        {
            "ALIAS": "default",
            'URL': 'mongodb://10.0.1.155/',
            'DB_NAME': 'test-mongo_mapper'
        }
    ])

print(get_id(IdType.Numeric, None))
print(get_id(IdType.Incremental, 'Hotel'))
print(get_id(IdType.Incremental, 'Hotel'))
print(get_id(IdType.Incremental, 'Hotel'))
print(get_id(IdType.Incremental, 'Hotel'))

print(get_id(IdType.ObjectId, 'Hotel'))
