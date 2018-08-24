from mongo_mapper.config import load_config
from mongo_mapper.document import DocumentRef
from mongo_mapper.exceptions import DocumentNotFound
from mongo_mapper.test.hotel import RoomBOCollection, Room


def __add_room(code, sub_code, name):
    room = Room()
    room.code = code
    room.sub_code = sub_code
    room.name = name
    room.save()
    print('Save object Room: {{code: {code}, sub_code: {sub_code}, name: {name}, id: {id} }}'.format(
        code=room.code,
        sub_code=room.sub_code,
        name=room.name,
        id=room.id)
    )
    return room


def __find_room(name):
    room_collection = RoomBOCollection()
    room_collection.fill_by_name(name)
    return room_collection


def run_test():
    load_config([
        {
            "ALIAS": "default",
            'URL': 'mongodb://10.0.1.155/',
            'DB_NAME': 'test-mongo_mapper'
        }
    ])

    for i in range(2):
        __add_room("room_{}".format(i), "sub_room_".format(i), "room_name")

    room_collection = __find_room("room_name")

    for room in room_collection:
        room.delete()


run_test()