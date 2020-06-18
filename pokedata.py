from json import dump, load
import poke_utils

class PokemonData(dict):
    def __init__(self, number: int, name: str, height: float, weight: float, types: list, abilities: list, egg_groups: list, final_exp: int, HP: int, Attack: int, Defence: int, SpAttack: int, SpDefence: int, Speed: int, OverAll: int, moves: list):
        self["number"] = number
        self["name"] = name
        self["height"] = height
        self["weight"] = weight
        self["types"] = types
        self["abilities"] = abilities
        self["eggGroups"] = egg_groups
        self["finalExp"] = final_exp
        self["HP"] = HP
        self["Attack"] = Attack
        self["Defence"] = Defence
        self["SpAttack"] = SpAttack
        self["SpDefence"] = SpDefence
        self["Speed"] = Speed
        self["OverAll"] = OverAll
        self["moves"] = moves

class PokemonMoves(dict):
    def __init__(self, id: int, name: str, types: str, category: int, power: int, accuracy: int, pp: int):
        self["id"] = id
        self["name"] = name
        int_types = poke_utils.get_int_types(types)
        self["types"] = int_types
        self["category"] = category
        self["power"] = power
        self["accuracy"] = accuracy
        self["pp"] = pp
        if category not in ["physical", "special"]:
            self["dynamax_power"] = 0
        else:
            self["dynamax_power"] = confirm_dynamax_power(name, int_types, power)
    
def confirm_dynamax_power(move_name, move_type, move_power):
    # 技固有のダイマックス時の威力を持つ場合
    with open("special_case_dynamax_power.json", encoding="utf-8") as f:
        special_list = load(f)
    
    for special_move in special_list:
        if move_name == special_move["name"]:
            return special_move["dynamax_power"]

    # 技の威力によってダイマックス時の威力を変更
    if move_power <= 40:
        if move_type not in [7, 8]:
            return 90
        else:
            return 70
    elif move_power <= 50:
        if move_type not in [7, 8]:
            return 100
        else:
            return 75
    elif move_power <= 60:
        if move_type not in [7, 8]:
            return 110
        else:
            return 80
    elif move_power <= 70:
        if move_type not in [7, 8]:
            return 120
        else:
            return 85
    elif move_power <= 100:
        if move_type not in [7, 8]:
            return 130
        else:
            return 90
    elif move_power <= 140:
        if move_type not in [7, 8]:
            return 140
        else:
            return 95
    else:
        if move_type not in [7, 8]:
            return 150
        else:
            return 100