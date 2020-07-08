from pokedata import PokemonData
import utils
import lxml.html
import re
import pokedex_exception
from bs4 import BeautifulSoup

# web_directry_string = 'https://pente.koro-pokemon.com/zukan/'
# pages_file = 'pokemon_url_list.txt'
# dex_filename = "pokedex.json"
# dex_list = []

# def main():
#     url = web_directry_string + page
#     html = utils.fetch_url(url)
#     get_pokemon(html, page, -1)
#     utils.save_json(dex_filename, dex_list)

def get_pokemon(html, page: str, int_id: int, section: int) -> dict:
    parsed_html = lxml.html.fromstring(html)

    # 図鑑番号と名前
    try:
        number = re.search(r'(\d+)' ,parsed_html.cssselect('#col1 > table.ta1.f10mpef14mpk > tbody > tr:nth-child(1) > th')[0].text)
        number = int(number.group(1))
        h1_text = parsed_html.cssselect('h1')[0].text
        name_full = re.search(r'(\w+)\s*(\(\w+\))', h1_text)
        if name_full is None:
            name = h1_text
            side_name = ""
        else:
            name = name_full.group(1)
            side_name = name_full.group(2)
        if name is None or side_name is None:
            raise pokedex_exception.Pokedex_Exception("Page = {0}, name or side_name Not Found.".format(page))
    except pokedex_exception.Pokedex_Exception:
        utils.except_logging(section)

    # ガラルに登場するか否か
    # try:
    #     on_galar = parsed_html.cssselect('#content_int > p > span')[0].text
    #     if str.startswith(on_galar, "[ガラル地方に登場"):
    #         on_galar = 1
    #     else:
    #         on_galar = 0
    # except pokedex_exception.Pokedex_Exception:
    #     utils.except_logging(section)
    
    # 禁止伝説か否か
    with open('banned_list.txt', encoding="utf-8") as f:
        lines = f.read().split('\n')
        if name in lines:
            banned = 1
        else:
            banned = 0

    # 高さ、重さ
    try:    
        height_weight_td = parsed_html.cssselect('#col1 > table.ta1.f10mpef14mpk > tbody > tr:nth-child(2) > td > table > tbody > tr > td.typec.zcat')[0].text_content()
        height_weight = re.findall(r'(\d+.\d+)', height_weight_td)
        if len(height_weight) == 2:
            height = float(height_weight[0])
            weight = float(height_weight[1])
        else:
            height = -1.0
            weight = -1.0
            raise pokedex_exception.SizeNotFound("Height or Weight Not Found. Page = {0}".format(page))
    except pokedex_exception.Pokedex_Exception:
        utils.except_logging(section)

    # タイプ
    try:
        types_href = parsed_html.cssselect('#col1 > table.ta1.f10mpef14mpk > tbody > tr:nth-child(2) > td > table > tbody > tr > td.typec.zcat > a')
        types = []
        for a in types_href:
            a_type = re.search(r'data/type-(\d+)', a.get('href'))
            types.append(int(a_type.group(1)))    
        if len(types) < 1 or len(types) > 2:
            types = [-1]
            raise pokedex_exception.PropertyLength_Exception("Types Not Found in href. Page = {0}".format(page))
    except pokedex_exception.PropertyLength_Exception:
        utils.except_logging(section)
    
    # 特性
    try:
        abilities = []
        abilities_td = parsed_html.cssselect('#col1 > table.ta1.f10mpef14mpk > tbody > tr > td.wsm121414m')
        for ability in abilities_td:
            ability_name = ability.text
            if ability_name != '-':
                ability_id = utils.number_property(1, ability_name)
                if ability_id == None:
                    abilities.append(-1)
                    raise pokedex_exception.AbilityID_NotFound("Page = {0}, Ability = {1}.".format(page, ability_name))
                else:
                    abilities.append(ability_id)
        if len(abilities) < 1 or len(abilities) > 3:
            raise pokedex_exception.PropertyLength_Exception
    except pokedex_exception.PropertyLength_Exception:
        utils.except_logging(section)
    except pokedex_exception.AbilityID_NotFound:
        utils.except_logging(section)

    # 最終経験値, タマゴグループ
    try:
        final_exp = parsed_html.cssselect("#col1 > table.ta1.f10mpef14mpk > tbody > tr > td.f12m")[-6].text
        if str.isdecimal(final_exp):
            final_exp = int(final_exp)
        else:
            final_exp = -1
            raise pokedex_exception.Pokedex_Exception("Final Exp Not Found. Page = {0}".format(page))
    except pokedex_exception.Pokedex_Exception:
        utils.except_logging(section)

    try:
        egg_groups_href = parsed_html.cssselect("#col1 > table.ta1.f10mpef14mpk > tbody > tr > td.f12m > a")
        egg_groups = []
        for a in egg_groups_href:
            a_egg = re.search(r'data/tamago-group-(\d+)', a.get('href'))
            egg_groups.append(int(a_egg.group(1)))
        if len(egg_groups) < 1:
            egg_groups = [-1]
            raise pokedex_exception.PropertyLength_Exception("Egg Group(s) error. Page = {0}".format(page))
    except pokedex_exception.Pokedex_Exception:
        utils.except_logging(section)
        
    # スタッツ
    try:
        HP = int(parsed_html.cssselect('#col1 > table.ta1.f10mpef14mpk > tbody > tr:nth-child(4) > td:nth-child(1) > table > tbody > tr:nth-child(1) > td:nth-child(2)')[0].text)
        Attack = int(parsed_html.cssselect('#col1 > table.ta1.f10mpef14mpk > tbody > tr:nth-child(4) > td:nth-child(1) > table > tbody > tr:nth-child(2) > td:nth-child(2)')[0].text)
        Defence = int(parsed_html.cssselect('#col1 > table.ta1.f10mpef14mpk > tbody > tr:nth-child(4) > td:nth-child(1) > table > tbody > tr:nth-child(3) > td:nth-child(2)')[0].text)
        SpAttack = int(parsed_html.cssselect('#col1 > table.ta1.f10mpef14mpk > tbody > tr:nth-child(4) > td:nth-child(1) > table > tbody > tr:nth-child(4) > td:nth-child(2)')[0].text)
        SpDefence = int(parsed_html.cssselect('#col1 > table.ta1.f10mpef14mpk > tbody > tr:nth-child(4) > td:nth-child(1) > table > tbody > tr:nth-child(5) > td:nth-child(2)')[0].text)
        Speed = int(parsed_html.cssselect('#col1 > table.ta1.f10mpef14mpk > tbody > tr:nth-child(4) > td:nth-child(1) > table > tbody > tr:nth-child(6) > td:nth-child(2)')[0].text)
        OverAll = int(parsed_html.cssselect('#col1 > table.ta1.f10mpef14mpk > tbody > tr:nth-child(4) > td:nth-child(1) > table > tbody > tr:nth-child(7) > td:nth-child(2)')[0].text)
    except IndexError:
        HP = -1
        Attack = -1
        Defence = -1
        SpAttack = -1
        SpDefence = -1
        Speed = -1
        OverAll = -1
        utils.except_logging(section)
    except ValueError:
        HP = -1
        Attack = -1
        Defence = -1
        SpAttack = -1
        SpDefence = -1
        Speed = -1
        OverAll = -1
        utils.except_logging(section)

    # ガラルに登場するか否か, 覚える技
    moveset = get_moves(html, page, section)
    if moveset[0]:
        on_galar = 0
    else:
        on_galar = 1
    moves = moveset[1]
    
    # 読み込み終えたら辞書として値を格納
    one_pokemon = PokemonData(number, int_id, name, side_name, on_galar, banned, height, weight, types, abilities, egg_groups, final_exp, HP, Attack, Defence, SpAttack, SpDefence, Speed, OverAll, moves)

    return one_pokemon

# ポケモンが覚える技のリストを取得する
def get_moves(html, page, section):
    soup = BeautifulSoup(html, 'html.parser')
    td_moves = soup.select('#waza4 > table  tbody > tr > td:nth-child(2)')
    sm_moves = False
    if len(td_moves) == 0:
        td_moves = soup.select('#waza3 > table  tbody > tr > td:nth-child(2)')
        sm_moves = True
    moves = []
    for move in td_moves:
        try:
            move_name = move.text
            move_id = utils.number_property(2, move_name)
            if move_id not in moves:
                if move_id == None and not sm_moves:
                    raise pokedex_exception.MoveID_NotFound("Page = {0}, Move = {1}".format(page, move_name))
                elif move_id != None:
                    moves.append(move_id)
        except pokedex_exception.MoveID_NotFound:
            utils.except_logging(section)
    moves.sort()
    return (sm_moves, moves)

# if __name__ == "__main__":
#     main()