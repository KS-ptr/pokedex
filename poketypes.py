# タイプとIDの関係を示すJSONファイルをダンプするスクリプト
import lxml.html
import json
import urllib.request
import re

url = 'https://pente.koro-pokemon.com/data/type.shtml'
json_filename = "poke_types.json"
types = []

def main():
    html = fetch(url)
    process(html)
    save(json_filename)

def fetch(url):
    header = {"User-Agent": "Mozzila/5.0"}
    req = urllib.request.Request(url, headers=header)
    res = urllib.request.urlopen(req)

    encoding = res.info().get_content_charset(failobj="utf-8")
    html = res.read().decode(encoding=encoding)

    return html

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

def save(filename):
    with open(filename, mode="w", encoding="utf-8") as f:
        json.dump(types, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(",", ": "))

if __name__ == "__main__":
    main()