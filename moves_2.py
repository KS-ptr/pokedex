from pokedata import Move_Target
import pokedex_exception
import utils
import lxml.html
from json import load

json_filename = "moves.json"
new_moves_list = []

def main():
    for i in range(1, 11):
        url = 'https://pente.koro-pokemon.com/data/waza-list-{0}.shtml'.format(i)
        html = utils.fetch_url(url)
        process(html)
    
    utils.save_json(json_filename, new_moves_list)

def process(html):
    moves_list_prep = []
    parsed_html = lxml.html.fromstring(html)
    moves_table = parsed_html.cssselect('#leftcontent > table > tbody > tr')
    for move_tr in moves_table:
        if len(move_tr) == 1:
            continue
        else:
            move_dict = {}
            try:
                move_name = move_tr[0].text_content()
                move_target = str.strip(move_tr[6].text)
                if move_target == "1匹選択":
                    move_target = Move_Target.Single
                elif move_target == "相手全体":
                    move_target = "All_Foe"
                elif move_target == "味方全体":
                    move_target = "All_Allies"
                elif move_target == "味方1匹":
                    move_target = "Single_Ally"
                elif move_target == "自分":
                    move_target = "Self"
                elif move_target == "ランダム":
                    move_target = "Random"
                elif move_target in ["全体", "周囲全体"]:
                    move_target = "All"
                elif move_target == "味方場":
                    move_target = "Ally_Field"
                elif move_target == "相手場":
                    move_target = "Foe_Field"
                elif move_target == "全体場":
                    move_target = "Field"
                else:
                    raise pokedex_exception.Pokedex_Exception("Target Not Detected. Target said {0}. Move Name = {1}".format(move_target, move_name))
            except pokedex_exception.Pokedex_Exception:
                move_target = "None"
                utils.except_logging()
    
        move_contact = move_tr[7].text
        if move_contact == "○":
            move_contact = 1
        else:
            move_contact = 0

        if str.startswith(move_name, "のろい"):
            move_name = "のろい"
        move_dict["name"] = move_name
        move_dict["target"] = move_target
        move_dict["contact"] = move_contact
        moves_list_prep.append(move_dict)

    with open("moves_prep.json", encoding="utf-8") as f:
        moves_list = load(f)

    for move in moves_list:
        for move_sup in moves_list_prep:
            if move_sup["name"] == move["name"]:
                move["target"] = move_sup["target"]
                move["contact"] = move_sup["contact"]
                new_moves_list.append(move)
            else:
                continue

if __name__ == "__main__":
    main()