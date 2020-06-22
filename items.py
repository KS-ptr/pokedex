import utils
import lxml.html
import re

url = 'https://appmedia.jp/pokemon_swordshield/4161067'
items_list = []
json_filename = 'items.json'

def main():
    html = utils.fetch_url(url)
    process(html)
    utils.save(json_filename, items_list)

def process(html):
    html = html[html.find('対戦用のアイテムと効果と入手方法'):html.find('同じわざしか出せなくなる代わりに')]
    parsed_html = lxml.html.fromstring(html)
    items_table = parsed_html.cssselect('table > tbody > tr')
    item_id = 0
    for item_tr in items_table:
        item_dict = {}
        item_id += 1
        item_dict["id"] = item_id
        item_dict["name"] = str.strip(item_tr[0].text_content())
        items_list.append(item_dict)

if __name__ == "__main__":
    main()
