from json import dump, load
import urllib.request
import datetime
import traceback
import requests
import configparser

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
    res.close()
    return html

# ポケモンのデータをクローリングして取得する
def crawling(url_list: list):
    config = configparser.ConfigParser()
    config.read('config.ini')
    mail_address = config.get("User-Agent", "mail_address")
    ses = requests.Session()
    ses.headers.update({"User-Agent": "Mozzila/5.0@{0}".format(mail_address)})
    for url in url_list:
        res = ses.get(url)

# 特性、技の名前からIDを取得する
def number_property(property_type: int, name: str) -> int:
    # 取得する対象が特性の場合
    if property_type == 1:
        with open('abilities.json', encoding="utf-8") as af:
            ability_list = load(af)
            for ability in ability_list:
                if name == ability["name"]:
                    return ability["id"]
    # 取得する対象が技の場合
    else:
        with open('moves.json', encoding="utf-8") as af:
            move_list = load(af)
            for move in move_list:
                if name == move["name"]:
                    return move["id"]

# 取得したデータをJSON形式にダンプする
def save(filename, dict_list):
    with open(filename, mode="w", encoding="utf-8") as f:
        dump(dict_list, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(",", ": "))

# 例外をログ出力する
def except_logging():
    with open("exception.log", encoding="utf-8", mode="a") as ef:
        ef.write(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
        traceback.print_exc(file=ef)