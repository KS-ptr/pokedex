import lxml.html
from bs4 import BeautifulSoup
import re
import utils

evio_list = []

def main():
    html = utils.fetch_url('https://wiki.xn--rckteqa2e.com/wiki/%E9%80%B2%E5%8C%96%E8%A1%A8')
    process(html)

def process(html):
    soup = BeautifulSoup(html, 'html.parser')
    ev_table = soup.select('#mw-content-text > div > table > tbody > tr > td')

    for td in ev_table:
        parse_ul(td.ul)
        # print(td.ul.li.a.string)
        # for ul in td.ul:
        #     print(ul.li.a.string)
        #     parse_ul(ul)
    utils.save_json("eviolite.json", evio_list)

def parse_ul(ul):
    if ul.ul is not None:
        evio_list.append({"name": ul.li.a.string, "side_name": "", "eviolite": 1})
        parse_ul(ul.ul)
    else:
        evio_list.append({"name": ul.li.a.string, "side_name": "", "eviolite": 0})
            

if __name__ == "__main__":
    main()