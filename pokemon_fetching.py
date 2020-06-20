from pokedata import PokemonData
import utils
import lxml.html
import urllib.request
import json
import re
import sys
import pokedex_exception

web_directry_string = 'https://pente.koro-pokemon.com/zukan/'
# page = '001.shtml'
page = 'xy/pumpkaboo.shtml'
# page = "goruugu.shtml"
dex_filename = "pokedex.json"
dex_list = []

# メインの処理、ここをループさせる
def main():
    url = web_directry_string + page
    html = utils.fetch_url(url)
    process(html)
    utils.save(dex_filename ,dex_list)

# def fetch(url):
#     header = {"User-Agent": "Mozzila/5.0"}
#     req = urllib.request.Request(url=url, headers=header)
#     res = urllib.request.urlopen(req)

#     encoding = res.info().get_content_charset(failobj="utf-8")
#     html = res.read().decode(encoding=encoding)
#     return html

def process(html):
    parsed_html = lxml.html.fromstring(html)
    # 図鑑番号と名前
    try:
        number = re.search(r'(\d+)' ,parsed_html.cssselect('#col1 > table.ta1.f10mpef14mpk > tbody > tr:nth-child(1) > th')[0].text)
        number = int(number.group(1))
        name = parsed_html.cssselect('h1')[0].text
    except ValueError("Couldn't get Dex Number. Page = {0}".format(page)):
        utils.except_logging()

    # 高さ、重さ
    try:    
        height_weight_td = parsed_html.cssselect('#col1 > table.ta1.f10mpef14mpk > tbody > tr:nth-child(2) > td > table > tbody > tr > td.typec.zcat')[0].text_content()
        height_weight = re.findall(r'(\d+.\d+)', height_weight_td)
        if len(height_weight) == 2:
            height = float(height_weight[0])
            weight = float(height_weight[1])
        else:
            raise pokedex_exception.SizeNotFound("Height or Weight Not Found. Page = {0}".format(page))
    except pokedex_exception.Pokedex_Exception:
        utils.except_logging()
        return

    # タイプ
    try:
        types_href = parsed_html.cssselect('#col1 > table.ta1.f10mpef14mpk > tbody > tr:nth-child(2) > td > table > tbody > tr > td.typec.zcat > a')
        types = []
        for a in types_href:
            a_type = re.search(r'data/type-(\d+)', a.get('href'))
            types.append(int(a_type.group(1)))    
        if len(types) < 1 or len(types) > 2:
            raise pokedex_exception.PropertyLength_Exception("Types Not Found in href. Page = {0}".format(page))
    except pokedex_exception.PropertyLength_Exception:
        utils.except_logging()

    try:
        # 特性
        abilities = []
        abilities_href = parsed_html.cssselect('#col1 > table.ta1.f10mpef14mpk > tbody > tr > td.wsm121414m')
        for ability in abilities_href:
            abilities.append(ability.text)
        if len(abilities) < 1 or len(abilities) > 3:
            raise pokedex_exception.PropertyLength_Exception
    except pokedex_exception.PropertyLength_Exception:
        utils.except_logging()
    except pokedex_exception.AbilityID_NotFound:
        pass

    # 最終経験値, タマゴグループ
    try:
        exp_index = 16 + len(abilities)
        final_exp = int(parsed_html.cssselect("#col1 > table.ta1.f10mpef14mpk > tbody > tr > td.f12m")[exp_index].text)
    except ValueError("expected final_exp td is not showing number value. Page = {0}".format(page)):
        utils.except_logging()

    try:
        egg_groups_href = parsed_html.cssselect("#col1 > table.ta1.f10mpef14mpk > tbody > tr > td.f12m > a")
        egg_groups = []
        for a in egg_groups_href:
            a_egg = re.search(r'data/tamago-group-(\d+)', a.get('href'))
            egg_groups.append(int(a_egg.group(1)))
        if len(egg_groups) < 1:
            raise pokedex_exception.PropertyLength_Exception("Egg Group(s) error. Page = {0}".format(page))
    except pokedex_exception.Pokedex_Exception:
        utils.except_logging()
        
    # スタッツ
    try:
        HP = int(parsed_html.cssselect('#col1 > table.ta1.f10mpef14mpk > tbody > tr:nth-child(4) > td:nth-child(1) > table > tbody > tr:nth-child(1) > td:nth-child(2)')[0].text)
        Attack = int(parsed_html.cssselect('#col1 > table.ta1.f10mpef14mpk > tbody > tr:nth-child(4) > td:nth-child(1) > table > tbody > tr:nth-child(2) > td:nth-child(2)')[0].text)
        Defence = int(parsed_html.cssselect('#col1 > table.ta1.f10mpef14mpk > tbody > tr:nth-child(4) > td:nth-child(1) > table > tbody > tr:nth-child(3) > td:nth-child(2)')[0].text)
        SpAttack = int(parsed_html.cssselect('#col1 > table.ta1.f10mpef14mpk > tbody > tr:nth-child(4) > td:nth-child(1) > table > tbody > tr:nth-child(4) > td:nth-child(2)')[0].text)
        SpDefence = int(parsed_html.cssselect('#col1 > table.ta1.f10mpef14mpk > tbody > tr:nth-child(4) > td:nth-child(1) > table > tbody > tr:nth-child(5) > td:nth-child(2)')[0].text)
        Speed = int(parsed_html.cssselect('#col1 > table.ta1.f10mpef14mpk > tbody > tr:nth-child(4) > td:nth-child(1) > table > tbody > tr:nth-child(6) > td:nth-child(2)')[0].text)
        OverAll = int(parsed_html.cssselect('#col1 > table.ta1.f10mpef14mpk > tbody > tr:nth-child(4) > td:nth-child(1) > table > tbody > tr:nth-child(7) > td:nth-child(2)')[0].text)
    except ValueError("Stats Error. Page = {0}".format(page)):
        utils.except_logging()

    # 覚える技
    try:
        td_moves = parsed_html.cssselect('#waza4 > table > tbody > tr > td:nth-child(2)')
        moves = []
        for move in td_moves:
            if move.text not in moves:
                moves.append(move.text)
    except pokedex_exception.MoveID_NotFound("Page = {0}".format(page)):
        utils.except_logging()
    
    # 読み込み終えたら辞書として値を格納
    one_pokemon = PokemonData(number, name, height, weight, types, abilities, egg_groups, final_exp, HP, Attack, Defence, SpAttack, SpDefence, Speed, OverAll, moves)
        
    # リストに追加する
    dex_list.append(one_pokemon)

# def save(file, dlist):
#     with open(dex_filename, mode="w", encoding="utf-8") as f:
#         json.dump(dlist, f, ensure_ascii=False)

if __name__ == "__main__":
    main()