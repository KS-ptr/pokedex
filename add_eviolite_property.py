import utils
from json import load, dump

def main():
    section_list = [i for i in range(1, 11)]
    # section_list = [1]
    with open ("./result/eviolite.json", encoding="utf-8") as evf:
        evio_list = load(evf)
    for section in section_list:
        new_pokedex_list = []
        with open("./result/pokedex_{0}.json".format(str(section)), encoding="utf-8") as f:
            pokedex_list = load(f)
        
        for pokedex in pokedex_list:
            eviolite = -2
            for evio in evio_list:
                if pokedex["name"] == evio["name"] and pokedex["side_name"] == evio["side_name"]:
                    eviolite = evio["eviolite"]
            pokedex["eviolite"] = eviolite
            new_pokedex_list.append(pokedex)

        utils.save_json("./result/new_pokedex_{0}.json".format(str(section)), new_pokedex_list)

if __name__ == "__main__":
    main()