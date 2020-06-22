import lxml.html
import re
import utils

url_1 = 'https://pente.koro-pokemon.com/zukan/'
url_2 = 'https://pente.koro-pokemon.com/zukan/region-form.shtml'
url_3 = 'https://pente.koro-pokemon.com/zukan/multi-form.shtml'
url_list = []
txt_filename = 'pokemon_url_list.txt'

def main():
    html1 = utils.fetch_url(url_1)
    html2 = utils.fetch_url(url_2)
    html3 = utils.fetch_url(url_3)
    process1(html1)
    process2(html2)
    process3(html3)
    save(txt_filename, url_list)

def process1(html):
    parsed_html = lxml.html.fromstring(html)
    pokemon_li = parsed_html.cssselect('#content_in > div > ul.ul2 > li > a')
    for li in pokemon_li:
        url = str.lstrip(li.get('href'), '../zukan/')
        if url not in url_list:
            url_list.append(url)

def process2(html):
    parsed_html = lxml.html.fromstring(html)
    pokemon_li = parsed_html.cssselect('#sort_zno > div > ul.ul2 > li > a')
    for li in pokemon_li:
        url = str.lstrip(li.get('href'), '../zukan/')
        if url not in url_list:
            url_list.append(url)

def process3(html):
    parsed_html = lxml.html.fromstring(html)
    pokemon_tr = parsed_html.cssselect('#content_in > div > table.ta2 > tbody > tr > td > a')
    for tr_a in pokemon_tr:
        url = str.lstrip(tr_a.get('href'), '../zukan/')
        if url not in url_list:
            url_list.append(url)

def save(filename, list):
    with open(filename, mode="w", encoding="utf-8") as f:
        for url in url_list:
            f.write(url + "\n")

if __name__ == "__main__":
    main()