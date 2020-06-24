import lxml.html
import utils
import pokedex_exception
import urllib.request
import re
import json

url = 'https://wiki.xn--rckteqa2e.com/wiki/%E3%83%80%E3%82%A4%E3%83%9E%E3%83%83%E3%82%AF%E3%82%B9%E3%82%8F%E3%81%96'
json_filename = 'special_case_dynamax_power.json'
moves_list = []

def main():
    html = utils.fetch_url(url)
    process(html)
    utils.save_json(json_filename, moves_list)

def process(html):
    parsed_html = lxml.html.fromstring(html)
    for i in range(1, 5):
        moves_table1 = parsed_html.cssselect(('#mw-content-text > div > table.wikitable > tbody > tr:nth-child({0}) > td > table > tbody > tr').format(i))
        for move_tr in moves_table1:
            move = {}
            try:
                if str.isdecimal(str.strip(move_tr[3].text_content())):
                    move_name = str.strip(move_tr[0].text_content())
                    move_dynamax_power = int(move_tr[3].text_content())
                    move["name"] = move_name
                    move["dynamax_power"] = move_dynamax_power
                    moves_list.append(move)
            except IndexError:
                continue

if __name__ == "__main__":
    main()