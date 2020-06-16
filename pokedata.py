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