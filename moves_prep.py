import pokedata
import pokedex_exception
import lxml.html
import urllib.request
import re
import json

url = 'https://wiki.xn--rckteqa2e.com/wiki/%E3%82%8F%E3%81%96%E4%B8%80%E8%A6%A7_(%E7%AC%AC%E5%85%AB%E4%B8%96%E4%BB%A3)'
json_filename = 'poke_moves_prep.json'
moves_list = []

def main():
    html = fetch(url)
    process(html)
    save(json_filename)

def fetch(html):
    header = {"User-Agent": "Mozzila/5.0"}
    req = urllib.request.Request(url, headers=header)
    res = urllib.request.urlopen(req)

    encoding = res.info().get_content_charset(failobj="utf-8")
    html = res.read().decode(encoding)
    return html

def process(html):
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
            move = pokedata.PokemonMoves(move_id, move_name, move_type, move_category, move_power, move_accuracy, move_pp)
            moves_list.append(move)


def save(filename):
    with open(filename, mode="w", encoding="utf-8") as f:
        json.dump(moves_list, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(",", ": "))

if __name__ == "__main__":
    main()