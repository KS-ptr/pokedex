from pokedata import PokemonMoves
import utils
import pokedex_exception
import lxml.html
from json import load

url = 'https://wiki.xn--rckteqa2e.com/wiki/%E3%82%8F%E3%81%96%E4%B8%80%E8%A6%A7_(%E7%AC%AC%E5%85%AB%E4%B8%96%E4%BB%A3)'
json_filename = 'moves_prep.json'
moves_list = []

def main():
    html = utils.fetch_url(url)
    with open('remarked_moves.json', encoding="utf-8") as f:
        remarked_moves = load(f)
    process(html, remarked_moves)
    utils.save_json(json_filename, moves_list)

def process(html, remarked_moves):
    parsed_html = lxml.html.fromstring(html)
    moves_table = parsed_html.cssselect('#mw-content-text > div > table:nth-child(5) > tbody > tr')
    move_id = 0
    for move_tr in moves_table:
        if str.isdecimal(move_tr[2].text_content()) or move_tr[2].text_content() == "":
            move_id += 1
            move_name = str.strip(move_tr[0].text_content())
            move_type = str.strip(move_tr[1].text_content())
            move_category = str.strip(move_tr[5].text_content())
            if move_category == "物理":
                move_category = "physical"
            elif move_category == "特殊":
                move_category = "special"
            elif move_category == "変化":
                move_category = "non-damaging"
            else:
                move_category = "Missing"
            try:
                move_power = int(move_tr[2].text_content())
                move_accuracy = int(move_tr[3].text_content())
                move_pp = int(move_tr[4].text_content())
            except ValueError:
                move_power = -1
                move_accuracy = -1
                move_pp = -1
            
            remarks = []
            for key in remarked_moves.keys():
                if move_name in remarked_moves[key]:
                    remarks.append(key)
            
            move = PokemonMoves(move_id, move_name, move_type, move_category, move_power, move_accuracy, move_pp, remarks)
            moves_list.append(move)

if __name__ == "__main__":
    main()