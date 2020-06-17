import lxml.html
import urllib.request
import re
import json

url = 'https://wiki.xn--rckteqa2e.com/wiki/%E3%82%8F%E3%81%96%E4%B8%80%E8%A6%A7_(%E7%AC%AC%E5%85%AB%E4%B8%96%E4%BB%A3)'
json_filename = 'poke_moves.json'

def main():
    html = fetch(url)
    process(html)

def fetch():
    header = {"User-Agent": "Mozzila/5.0"}
    req = urllib.request.Request(url, headers=header)
    res = urllib.request.urlopen(req)

    encoding = res.info().get_content_charset(failobj="utf-8")
    html = res.read().decode(encoding)
    return html

def process(html):
    parsed_html = lxml.html.fromstring(html)


def save():
    pass

if __name__ == "__main__":
    main()