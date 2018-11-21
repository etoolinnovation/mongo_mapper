from mongo_mapper.config import load_config
from mongo_mapper.document import DocumentRef
from mongo_mapper.exceptions import DocumentNotFound
from mongo_mapper.test.hotel import RoomBOCollection, Room
import time

def __add_room(code, sub_code, name):
    room = __create_room(code, sub_code, name)
    room.save()
    print('Save object Room: {{code: {code}, sub_code: {sub_code}, name: {name}, id: {id} }}'.format(
        code=room.code,
        sub_code=room.sub_code,
        name=room.name,
        id=room.id)
    )
    return room

def __create_room(code, sub_code, name):
    room = Room()
    room.code = code
    room.sub_code = sub_code
    room.name = name
    return room

def __find_room(name):
    room_collection = RoomBOCollection()
    room_collection.fill_by_name(name)
    return room_collection


def run_test():
    start = time.time()
    load_config([
        {
            "ALIAS": "default",
            'URL': 'mongodb://10.0.1.155/',
            'DB_NAME': 'test-mongo_mapper'
        }
    ])
    print("Load config: {}".format(time.time() - start))
    start = time.time()
    for i in range(100):
        __add_room("room_{}".format(i), "sub_room_".format(i), "room_name")
    print("Add 100 rooms: {}".format(time.time() - start))

    start = time.time()
    room_collection = __find_room("room_name")

    for room in room_collection:
        room.delete()

    print("Delete 100 rooms: {}".format(time.time() - start))


    room_list = []
    for i in range(100):
        room_list.append(__create_room("room_{}".format(i), "sub_room_".format(i), "room_name"))

    start = time.time()
    room_list = Room.multi_insert(room_list)
    print("Add 100 multiple rooms: {}".format(time.time() - start))


run_test()
