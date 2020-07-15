from sys import argv
from bs4 import BeautifulSoup
import pokedex_exception
from utils import fetch_url, number_property, except_logging
# import 

prefix = "https://pente.koro-pokemon.com/zukan/"
suffix_list = ["xy/nyaonikusu.shtml", "swordshield/toxtricity.shtml", "swordshield/indeedee.shtml"]

def main():
    if argv[1] == "n":
        nyaonikusu()
    elif argv[1] == "t":
        toxtricity()
    elif argv[1] == "i":
        indeedee()

def nyaonikusu():
    male_moves = ["くろいまなざし", "ひっかく", "にらみつける", "ねこだまし", "チャームボイス", "ねんりき", "てだすけ", "あまえる", "ほしがる", "サイケこうせん", "ふいうち", "なりきり", "ひかりのかべ", "リフレクター", "サイコショック", "ふういん", "ファストガード", "サイコキネシス", "ミストフィールド", "ワイドフォース", "あくび", "くすぐる", "ネコにこばん", "はかいこうせん", "ギガインパクト", "でんじは", "あなをほる", "ひかりのかべ", "リフレクター", "しんぴのまもり", "ねむる", "いびき", "まもる", "あまえる", "あまごい", "にほんばれ", "からげんき", "スピードスター", "てだすけ", "ふういん", "うそなき", "しっぺがえし", "トリックルーム", "ワンダールーム", "マジックルーム", "りんしょう", "スイープビンタ", "ミストフィールド", "サイコフィールド", "10まんボルト", "サイコキネシス", "みがわり", "サイコショック", "こらえる", "ねごと", "アイアンテール", "シャドーボール", "トリック", "スキルスワップ", "めいそう", "あくのはどう", "エナジーボール", "わるだくみ", "しねんのずつき", "サイドチェンジ", "ふるいたてる", "じゃれつく"]
    female_moves = ["マジカルリーフ", "ひっかく", "にらみつける", "ねこだまし", "チャームボイス", "ねんりき", "アシストパワー", "チャージビーム", "ほしがる", "サイケこうせん", "ふいうち", "なりきり", "ひかりのかべ", "リフレクター", "サイコショック", "じんつうりき", "シャドーボール", "サイコキネシス", "みらいよち", "ワイドフォース", "あくび", "くすぐる", "ネコにこばん", "はかいこうせん", "ギガインパクト", "マジカルリーフ", "でんじは", "あなをほる", "ひかりのかべ", "リフレクター", "しんぴのまもり", "ねむる", "いびき", "まもる", "あまえる", "メロメロ", "あまごい", "にほんばれ", "からげんき", "スピードスター", "てだすけ", "うそなき", "しっぺがえし", "トリックルーム", "ワンダールーム", "マジックルーム", "りんしょう", "スイープビンタ", "サイコフィールド", "10まんボルト", "サイコキネシス", "みがわり", "サイコショック", "こらえる", "ねごと", "アイアンテール", "シャドーボール", "みらいよち", "トリック", "スキルスワップ", "めいそう", "あくのはどう", "エナジーボール", "わるだくみ", "しねんのずつき", "アシストパワー", "サイドチェンジ", "ふるいたてる", "じゃれつく"]

    print("male moveset:", set_moves_by_bruteforce(male_moves))
    print("female moves:", set_moves_by_bruteforce(female_moves))


def toxtricity():
    html = fetch_url(prefix + suffix_list[1])
    soup = BeautifulSoup(html, 'html.parser')
    teached_moves = soup.select("#waza4 > table:nth-child(7) > tbody > tr > td:nth-child(2)")
    egg_moves = soup.select("#waza4 > table:nth-child(9) > tbody > tr > td:nth-child(2)")
    machine_moves = soup.select("#waza4 > table:nth-child(11) > tbody > tr > td:nth-child(2)")
    record_moves = soup.select("#waza4 > table:nth-child(13) > tbody > tr > td:nth-child(2)")
    high_move1 = soup.select("#waza4 > table:nth-child(3) > tbody > tr > td:nth-child(2)")
    low_move1 = soup.select("#waza4 > table:nth-child(5) > tbody > tr > td:nth-child(2)")

    high_moves = []
    high_moves.extend(high_move1)
    high_moves.extend(teached_moves)
    high_moves.extend(egg_moves)
    high_moves.extend(machine_moves)
    high_moves.extend(record_moves)

    low_moves = []
    low_moves.extend(low_move1)
    low_moves.extend(teached_moves)
    low_moves.extend(egg_moves)
    low_moves.extend(machine_moves)
    low_moves.extend(record_moves)

    print("high moveset:", set_moves(high_moves))
    print("low moveset:", set_moves(low_moves))

def indeedee():
    with open("indeedee_male_moves.txt", "r", encoding="utf-8") as f:
        male_moves = f.read().splitlines()

    with open("indeedee_female_moves.txt", "r", encoding="utf-8") as f:
        female_moves = f.read().splitlines()

    print("male moveset:", set_moves_by_bruteforce(male_moves))
    print("female moveset:", set_moves_by_bruteforce(female_moves))

def set_moves(move_namelist):
    moves = []
    for move_td in move_namelist:
        try:
            move_name = move_td.text
            move_id = number_property(2, move_name)
            if move_id not in moves:
                if move_id == None:
                    raise pokedex_exception.MoveID_NotFound("Page = {0}, Move = {1}".format(argv[1], move_name))
                elif move_id != None:
                    moves.append(move_id)
        except pokedex_exception.MoveID_NotFound:
            except_logging(99)
    moves.sort()
    return moves

def set_moves_by_bruteforce(move_namelist):
    moves = []
    for move in move_namelist:
        move_id = number_property(2, move)
        if move_id not in moves:
            moves.append(move_id)
    moves.sort()
    return moves

if __name__ == "__main__":
    main()