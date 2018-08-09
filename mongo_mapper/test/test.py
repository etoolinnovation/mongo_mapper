from mongo_mapper.test.room import Room
from mongo_mapper.exceptions import DocumentNotFound


def run_test_room():
    room = Room()
    room.code = "code_1"
    room.code_dingus = "code_dingus_1"
    room.name = "name_1"
    room.save()
    print('Save object Room: {{code: {code}, code_dingus: {code_dingus}, name: {name}, id: {id} }}'.format(
        code=room.code,
        code_dingus=room.code_dingus,
        name=room.name,
        id=room.id)
    )

    room1 = Room()
    room1.find_by_pk("code_1", "code_dingus_1")
    print('Find object Room by PK: {{code: {code}, code_dingus: {code_dingus}, name: {name}, id: {id} }}'.format(
        code=room1.code,
        code_dingus=room1.code_dingus,
        name=room1.name,
        id=room1.id)
    )

    print('Delete object Room: {{code: {code}, code_dingus: {code_dingus}, name: {name}, id: {id} }}'.format(
        code=room1.code,
        code_dingus=room1.code_dingus,
        name=room1.name,
        id=room1.id)
    )
    room1.delete()

    try:
        room1.find_by_pk("code_1", "code_dingus_1")
    except DocumentNotFound as e:
        print('Find object Room by PK raise: {}'.format(e))


run_test_room()
