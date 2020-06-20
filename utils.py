from json import dump, load
import urllib.request
import datetime
import traceback
import json

# タイプの文字列からタイプのインデックスを取得する
def get_int_types(str_types) -> int:
    if str_types == "":
        return 0
    with open('types.json', encoding="utf-8") as f:
        types_list = load(f)
        for types in types_list:
            if types["name"] == str_types:
                return int(types["id"])

# Webからhtmlを取得する
def fetch_url(url):
    header = {"User-Agent": "Mozzila/5.0"}
    req = urllib.request.Request(url, headers=header)
    res = urllib.request.urlopen(req)

    encoding = res.info().get_content_charset(failobj="utf-8")
    html = res.read().decode(encoding)
    return html

# 取得したデータをJSON形式にダンプする
def save(filename, dict_list):
    with open(filename, mode="w", encoding="utf-8") as f:
        json.dump(dict_list, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(",", ": "))

# 例外をログ出力する
def except_logging():
    with open("exception.log", encoding="utf-8", mode="a") as ef:
        ef.write(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
        traceback.print_exc(file=ef)