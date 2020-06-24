# タイプとIDの関係を示すJSONファイルをダンプするスクリプト
import utils
import lxml.html
import re

url = 'https://pente.koro-pokemon.com/data/type.shtml'
json_filename = "types.json"
types = []

def main():
    html = utils.fetch_url(url)
    process(html)
    utils.save_json(json_filename, types)

def process(html):
    parsed_html = lxml.html.fromstring(html)
    types_html = parsed_html.cssselect('#content_in > ul.ul1 > li > a')
    for type_html in types_html:
        if "タイプ" in type_html.text:
            types_dict = {}
            types_id = re.search(r'(\d+)', type_html.get('href'))
            types_id = types_id.group(1)
            types_name = type_html.text.rstrip("タイプ")
            types_dict["id"] = types_id
            types_dict["name"] = types_name
            types.append(types_dict)
        else:
            continue

if __name__ == "__main__":
    main()