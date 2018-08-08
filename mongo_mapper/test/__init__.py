from mongo_mapper.test.room import Room


def run_test():
    room = Room()
    room.code = "code_1"
    room.name = "name_1"
    room.save()
    print('Save object Room: {{code: {code}, name: {name} }}'.format(code=room.code, name=room.name))

    room1 = Room()
    room1.find_by_pk("code_1", "name_1")
    print('Find object Room by PK: {{code: {code}, name: {name} }}'.format(code=room1.code, name=room1.name))


# run_test()