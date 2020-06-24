import utils
from get_pokemon import get_pokemon
from requests import Session

dex_list = []

def main():
    url_list = get_urllist()
    # crawling(url_list)
    # utils.save_json(filename, dex_list)

def get_urllist():
    with open('pokemon_url_list.txt', encoding="utf-8") as f:
        return f.read().split('\n')

# ポケモンのデータをクローリングして取得する
def crawling(url_list: list):
    ses = Session()
    ses.headers.update({"User-Agent": "Mozzila/5.0"})
    for url in url_list:
        res = ses.get(url)
        encoding = res.apparent_encoding
        html = res.content.decode(encoding=encoding)
        dex_list.append(get_pokemon(html))

if __name__ == "__main__":
    main()