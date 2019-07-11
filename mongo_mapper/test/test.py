from mongo_mapper.config import load_config
from mongo_mapper.document import DocumentRef, DocumentRefExtended
from mongo_mapper.exceptions import DocumentNotFound
from mongo_mapper.test.hotel import Room, RoomCol, Extra, Hotel


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


def __delete_room(room):
    print('Delete object Room: {{code: {code}, code_dingus: {code_dingus}, name: {name}, id: {id} }}'.format(
        code=room.code,
        code_dingus=room.sub_code,
        name=room.name,
        id=room.id)
    )
    room.delete()


def __add_extra(code, sub_code, name):
    extra = Extra()
    extra.code = code
    extra.sub_code = sub_code
    extra.name = name
    print('Create object Extra: {{code: {code}, sub_code: {sub_code}, name: {name} }}'.format(
        code=extra.code,
        sub_code=extra.sub_code,
        name=extra.name)
    )
    return extra


def __find_room(code, sub_code):
    room = Room()
    try:
        room.find_by_pk(code, sub_code)
        print('Find object Room by PK: {{code: {code}, sub_code: {sub_code}, name: {name}, id: {id} }}'.format(
            code=room.code,
            sub_code=room.sub_code,
            name=room.name,
            id=room.id)
        )
        return room
    except DocumentNotFound as e:
        print('Find object Room {{code: {code}, sub_code: {sub_code}, name: {name}, id: {id} }} by PK raise: {ex}'.
            format(
            code=room.code,
            sub_code=room.sub_code,
            name=room.name,
            id=room.id,
            ex=e
        ))


def run_test():
    load_config([
        {
            "ALIAS": "default",
            'URL': 'mongodb://10.0.1.155/',
            'DB_NAME': 'test-mongo_mapper'
        }
    ])

    Room.create_indexes(True)

    __add_room("room_1", "sub_room_1", "room_name_1")
    __add_room("room_2", "sub_room_2", "room_name_2")
    room1 = __find_room("room_1", "sub_room_1")
    room2 = __find_room("room_2", "sub_room_2")

    col_room = RoomCol()
    col_room.find_by_name("name")

    print("Find collection Room: {}".format(col_room.to_list()))

    Hotel.create_indexes(True)

    hotel = Hotel()
    hotel.code = "hotel_1"
    hotel.sub_code = "sub_hotel_1"
    hotel.rooms = [
        DocumentRef(room1).db_ref,
        DocumentRef(room2).db_ref,
    ]

    room1_extended = DocumentRefExtended(room1)
    room1_extended.sub_code = "modified by document ref extended"

    hotel.rooms_extended = [
        room1_extended
    ]

    extra1 = __add_extra("extra_1", "sub_extra_1", "extra_name_1")
    extra2 = __add_extra("extra_2", "sub_extra_2", "extra_name_2")
    hotel.extras = [
        extra1.to_dict(),
        extra2.to_dict()
    ]

    hotel.save()
    print(
        'Save object Hotel: {{code: {code}, sub_code: {sub_code}, id: {id}, rooms:{rooms}, extras: {extras} }}'.format(
            code=hotel.code,
            sub_code=hotel.sub_code,
            id=hotel.id,
            rooms=hotel.rooms,
            extras=hotel.extras)
    )

    __delete_room(room1)
    __delete_room(room2)

    __find_room("room_1", "sub_room_1")
    __find_room("room_2", "sub_room_2")

    print(
        'Delete object Hotel: {{code: {code}, sub_code: {sub_code}, id: {id}, rooms:{rooms}, extras: {extras} }}'.format(
            code=hotel.code,
            sub_code=hotel.sub_code,
            id=hotel.id,
            rooms=hotel.rooms,
            extras=hotel.extras)
    )

    hotel.delete()


run_test()
