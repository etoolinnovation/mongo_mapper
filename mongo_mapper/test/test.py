from mongo_mapper.test.hotel import Room, Extra, Hotel
from mongo_mapper.exceptions import DocumentNotFound
from mongo_mapper.document import DocumentRef


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
    room.find_by_pk(code, sub_code)
    print('Find object Room by PK: {{code: {code}, sub_code: {sub_code}, name: {name}, id: {id} }}'.format(
        code=room.code,
        sub_code=room.sub_code,
        name=room.name,
        id=room.id)
    )
    return room


def run_test():
    __add_room("room_1", "sub_room_1", "room_name_1")
    __add_room("room_2", "sub_room_2", "room_name_2")
    room1 = __find_room("room_1", "sub_room_1")
    room2 = __find_room("room_2", "sub_room_2")

    hotel = Hotel()
    hotel.code = "hotel_1"
    hotel.sub_code = "sub_hotel_1"
    hotel.rooms = [
        DocumentRef(room1).db_ref,
        DocumentRef(room2).db_ref,
    ]

    extra1 = __add_extra("extra_1", "sub_extra_1", "extra_name_1")
    extra2 = __add_extra("extra_2", "sub_extra_2", "extra_name_2")
    hotel.extras = [
        extra1.to_dict(),
        extra2.to_dict()
    ]

    hotel.save()
    print('Save object Hotel: {{code: {code}, sub_code: {sub_code}, id: {id}, rooms:{rooms}, extras: {extras} }}'.format(
        code=hotel.code,
        sub_code=hotel.sub_code,
        id=hotel.id,
        rooms=hotel.rooms,
        extras=hotel.extras)
    )

    # print('Delete object Room: {{code: {code}, code_dingus: {code_dingus}, name: {name}, id: {id} }}'.format(
    #     code=room1.code,
    #     code_dingus=room1.sub_code,
    #     name=room1.name,
    #     id=room1.id)
    # )
    # room1.delete()

    # try:
    #     room1.find_by_pk("code_1", "code_dingus_1")
    # except DocumentNotFound as e:
    #     print('Find object Room by PK raise: {}'.format(e))


run_test()
