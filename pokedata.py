from json import dump

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
    def __init__(self, id: int, name: str, types: int, category: int, power: int, accuracy: int, pp: int, dynamax_power: int):
        self["name"] = name
        self["types"] = types
        self["category"] = category
        self["power"] = power
        self["accuracy"] = accuracy
        self["pp"] = pp
        # 技固有のダイマックス時の威力を持つ場合
        # 技の威力によってダイマックス時の威力を変更
        if power <= 40:
            if types not in [7, 8]:
                self["dynamax_power"] = 90
            else:
                self["dynamax_power"] = 70
        elif power <= 50:
            if types not in [7, 8]:
                self["dynamax_power"] = 100
            else:
                self["dynamax_power"] = 75
        elif power <= 60:
            if types not in [7, 8]:
                self["dynamax_power"] = 110
            else:
                self["dynamax_power"] = 80
        elif power <= 70:
            if types not in [7, 8]:
                self["dynamax_power"] = 120
            else:
                self["dynamax_power"] = 85
        elif power <= 100:
            if types not in [7, 8]:
                self["dynamax_power"] = 130
            else:
                self["dynamax_power"] = 90
        elif power <= 140:
            if types not in [7, 8]:
                self["dynamax_power"] = 140
            else:
                self["dynamax_power"] = 95
        else:
            if types not in [7, 8]:
                self["dynamax_power"] = 150
            else:
                self["dynamax_power"] = 100