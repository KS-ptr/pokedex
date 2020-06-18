from json import dump, load
import datetime
import traceback

def get_int_types(str_types) -> int:
    if str_types == "":
        return 0
    with open('poke_types.json', encoding="utf-8") as f:
        types_list = load(f)
        for types in types_list:
            if types["name"] == str_types:
                return int(types["id"])

def except_logging():
    with open("exception.log", encoding="utf-8", mode="a") as ef:
        ef.write(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
        traceback.print_exc(file=ef)