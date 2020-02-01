import json
import time


# Special abilities to load from one spot.

def change_to_norm(nora):
    # Circular imports are an unfortunate thing...
    from character import Character
    from game import CHARACTERS_DIR

    # Gross, I know, but I also don't want the opponent to do this
    # extra times.
    if nora.name == 'Norm':
        return

    namepath = f"{CHARACTERS_DIR}/nora/norm"
    with open(f"{namepath}/magic.json", "r") as magic_fl, \
         open(f"{namepath}/taunts.json", "r") as taunts_fl:
        magic_info = json.load(magic_fl)
        taunts = json.load(taunts_fl)

    norm = Character(
        name="Norm",
        bio="It's a long story, to be honest.",
        magic_info=magic_info,
        taunts=taunts
    )

    print('Nora becomes Norm!')
    time.sleep(1)

    return norm
