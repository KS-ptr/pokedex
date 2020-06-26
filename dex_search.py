from sys import argv
from json import load
from math import ceil

def main():
    if str.isdecimal(argv[1]):
        dex_no = int(argv[1])
        search(dex_no, 1)
    else:
        dex_name = argv[1]
        search(dex_name, 2)

def search(search_term, condition):
    section = ceil(search_term / 100)
    with open('pokedex_{0}.json'.format(section), encoding="utf-8") as f:
        dex_list = load(f)
        for dex in dex_list:
            if condition == 1:
                if search_term == dex["id"]:
                    result = dex
            else:
                if search_term == dex["name"]:
                    result = dex
    show_dex(result)

def show_dex(dex):
    dex_moves = []
    with open('moves.json', encoding="utf-8") as f:
        moves_list = load(f)
        for move in moves_list:
            if move["id"] in dex["moves"]:
                dex_moves.append(move["name"])
    dex_abilities = []
    with open('abilities.json', encoding="utf-8") as f:
        abilities_list = load(f)
        for ability in abilities_list:
            if ability["id"] in dex["abilities"]:
                dex_abilities.append(ability["name"])
    dex_types = []
    with open('types.json', encoding="utf-8") as f:
        types_list = load(f)
        for poke_type in types_list:
            if poke_type["id"] in dex["types"]:
                dex_types.append(poke_type["name"])
    print('Dex No : ', dex["number"])
    print('Name : ', dex["name"] + dex["side_name"])
    print('Type(s) : ', dex_types)
    print('abilities : ', dex_abilities)
    print('HP : ', dex["HP"])
    print('Attack : ', dex["Attack"])
    print('Defence : ', dex["Defence"])
    print('Sp-Attack : ', dex["SpAttack"])
    print('Sp-Defence : ', dex["SpDefence"])
    print('Speed : ', dex["Speed"])
    print('moves : ', dex_moves)

if __name__ == "__main__":
    main()