import lxml.html
import utils
import re

url = 'https://wiki.xn--rckteqa2e.com/wiki/%E3%81%A8%E3%81%8F%E3%81%9B%E3%81%84%E4%B8%80%E8%A6%A7'
abilities_list = []
json_filename = 'abilities.json'

def main():
    html = utils.fetch_url(url)
    process(html)
    utils.save_json(json_filename, abilities_list)

def process(html):
    parsed_html = lxml.html.fromstring(html)
    abilities_table = parsed_html.cssselect('#mw-content-text > div > table > tbody > tr')
    for ability_tr in abilities_table:
        ability = {}
        ability_id = str.strip(ability_tr[0].text_content())
        if str.isdecimal(ability_id):
            ability_id = int(ability_id)
        elif ability_id == "":
            ability_id = -1
        else:
            continue
        ability_name = str.strip(ability_tr[1].text_content())
        ability["id"] = ability_id
        ability["name"] = ability_name
        abilities_list.append(ability)

if __name__ == "__main__":
    main()