import utils
import lxml.html
import re

url_sound = 'https://wiki.xn--rckteqa2e.com/wiki/%E3%82%AB%E3%83%86%E3%82%B4%E3%83%AA:%E9%9F%B3%E3%81%AE%E3%82%8F%E3%81%96'
url_biting = 'https://wiki.xn--rckteqa2e.com/wiki/%E3%82%AB%E3%83%86%E3%82%B4%E3%83%AA:%E3%81%8B%E3%81%BF%E3%81%A4%E3%81%8D%E3%82%8F%E3%81%96'
url_bullet = 'https://wiki.xn--rckteqa2e.com/wiki/%E3%82%AB%E3%83%86%E3%82%B4%E3%83%AA:%E5%BC%BE%E3%81%AE%E3%82%8F%E3%81%96'
url_punch = 'https://wiki.xn--rckteqa2e.com/wiki/%E3%82%AB%E3%83%86%E3%82%B4%E3%83%AA:%E3%83%91%E3%83%B3%E3%83%81%E3%82%8F%E3%81%96'
url_reckless = 'https://wiki.xn--rckteqa2e.com/wiki/%E3%81%99%E3%81%A6%E3%81%BF'
url_pulse = 'https://wiki.xn--rckteqa2e.com/wiki/%E3%83%A1%E3%82%AC%E3%83%A9%E3%83%B3%E3%83%81%E3%83%A3%E3%83%BC'
url_sheer_force = 'https://wiki.xn--rckteqa2e.com/wiki/%E8%BF%BD%E5%8A%A0%E5%8A%B9%E6%9E%9C'
moves_dict = {}

def main():
    html1 = utils.fetch_url(url_sound)
    html2 = utils.fetch_url(url_biting)
    html3 = utils.fetch_url(url_bullet)
    html4 = utils.fetch_url(url_punch)
    html5 = utils.fetch_url(url_reckless)
    html6 = utils.fetch_url(url_pulse)
    process(html1, "sound", '#mw-pages > div > div > div > ul > li > a')
    process(html2, "biting", '#mw-pages > div > div > div > ul > li > a')
    process(html3, "bullet", '#mw-pages > div > div > div > ul > li > a')
    process(html4, "punch", '#mw-pages > div > div > div > ul > li > a')
    process(html5, "reckless", '#mw-content-text > div > ul:nth-child(4) > li:nth-child(2) > ul > li > a')
    process(html6, "pulse", '#mw-content-text > div > ul:nth-child(4) > li:nth-child(1) > ul > li > a')
    html7 = utils.fetch_url(url_sheer_force)
    process2(html7, "sheer_force")
    utils.save_json("remarked_moves.json", moves_dict)

def process(html, feature: str, selector):
    parsed_html = lxml.html.fromstring(html)
    moves = parsed_html.cssselect(selector)
    move_list = []
    for move in moves:
        move_name = move.text
        if move_name not in move_list:
            move_list.append(move_name)
    moves_dict[feature] = move_list

def process2(html, feature: str):
    parsed_html = lxml.html.fromstring(html)
    move_list = []
    moves = parsed_html.cssselect('#mw-content-text > div > dl:nth-child(12) > dd > table > tbody > tr > th > a')
    for move in moves[8:]:
        move_name = move.get('title')
        if move_name not in move_list:
            move_list.append(move_name)
    
    moves = parsed_html.cssselect('#mw-content-text > div > table:nth-child(15) > tbody > tr> th > a')
    for move in moves[8:]:
        move_name = move.get('title')
        if move_name not in move_list:
            move_list.append(move_name)

    for i in range(1, 3):
        for j in range(1, 5):
            moves = parsed_html.cssselect('#mw-content-text > div > table.wikitable > tbody > tr:nth-child({0}) > td:nth-child({1}) > table > tbody > tr> th > a'.format(str(i), str(j)))
            for move in moves:
                move_name = move.get('title')
                if move_name not in move_list:
                    move_list.append(move_name)

    moves = parsed_html.cssselect('#mw-content-text > div > dl:nth-child(22) > dd > table > tbody > tr > th > a')
    for move in moves:
        move_name = move.get('title')
        if move_name not in move_list:
            move_list.append(move_name)
    moves_dict[feature] = move_list

if __name__ == "__main__":
    main()