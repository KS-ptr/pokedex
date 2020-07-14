#!/bin/bash

#pipenv shell
python3 abilities.py
#echo "abilities.json done."
python3 get_types.py
#echo "types.json done."
python3 moves_with_remarks.py
#echo "remarked_moves.json done."
python3 moves_prep.py
#echo "moves_prep.json done."
python3 moves_2.py
#echo "moves.json done."
python3 get_pagelist.py
#echo "pokemon_page_list.txt done."

for i in {1..10} ; do
    python3 crawling.py ${i}
done
