import json

default = 'database/default/gcide_'
custom = 'database/custom'

ascii = 97
for i in range(26):
    with open(default + chr(ascii + i) + '.json') as file:
        json_file: dict = json.load(file)
        full_list = json_file.items()
        for j in range():
            print(json_file["a"])
