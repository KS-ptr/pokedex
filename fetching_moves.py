from pokedata import PokemonData
import utils
from bs4 import BeautifulSoup
import re
import pokedex_exception

web_directry_string = 'https://pente.koro-pokemon.com/zukan/'
page = 'hihidaruma.shtml'

def main():
    url = web_directry_string + page
    html = utils.fetch_url(url)
    process(html)

def process(html):
    soup = BeautifulSoup(html, 'html.parser')
    td_moves = soup.select('#waza4 > table > tbody > tr > td:nth-child(2)')
    moves = []
    for move in td_moves:
        try:
            move_name = move.text
            move_id = utils.number_property(2, move_name)
            if move_id not in moves:
                if move_id == None:
                    raise pokedex_exception.MoveID_NotFound("Page = {0}, Move = {1}".format(page, move_name))
                else:
                    moves.append(move_id)
        except pokedex_exception.MoveID_NotFound:
            utils.except_logging(0)
    moves.sort()

if __name__ == "__main__":
    main()