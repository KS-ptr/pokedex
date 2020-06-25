import utils
from get_pokemon import get_pokemon
from requests import Session
from sys import argv
from time import sleep

dex_list = []
filename = "pokedex_{0}.json".format(argv[1])
web_directry_string = 'https://pente.koro-pokemon.com/zukan/'

def main():
    page_list = get_urllist(int(argv[1]))
    crawling(page_list)
    utils.save_json(filename, dex_list)

def get_urllist(section_number: int):
    with open('pokemon_page_list.txt', encoding="utf-8") as f:
        page_list = f.read().split('\n')
        if section_number < 1 or (section_number - 1) * 100 > len(page_list):
            print('Out of Range.')
            exit()
        elif section_number * 100 < len(page_list):
            return page_list[(section_number - 1) * 100 : section_number * 100 - 1]
        else:
            return page_list[(section_number - 1) * 100 : -1]

# ポケモンのデータをクローリングして取得する
def crawling(page_list: list):
    ses = Session()
    ses.headers.update({"User-Agent": "Mozzila/5.0"})
    for page in page_list:
        url = web_directry_string + page
        res = ses.get(url)
        encoding = res.apparent_encoding
        html = res.content.decode(encoding=encoding)
        dex_list.append(get_pokemon(html, page))
        sleep(0.5)

if __name__ == "__main__":
    main()