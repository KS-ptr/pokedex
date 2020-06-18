from json import dump, load

def get_int_types(str_types) -> int:
    if str_types == "":
        return 0
    with open('poke_types.json', encoding="utf-8") as f:
        types_list = load(f)
        for types in types_list:
            if types["name"] == str_types:
                return int(types["id"])