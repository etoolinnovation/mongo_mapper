from mongo_mapper.core.id_manager import IdType, get_id

print(get_id(IdType.Numeric, None))
print(get_id(IdType.Incremental, 'Hotel'))
print(get_id(IdType.Incremental, 'Hotel'))
print(get_id(IdType.Incremental, 'Hotel'))
print(get_id(IdType.Incremental, 'Hotel'))

print(get_id(IdType.ObjectId, 'Hotel'))