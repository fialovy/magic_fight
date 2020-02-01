import json

from character import Character

# Special abilities to load from one spot.

# Honora
def change_to_norm(nora):
    from game import CHARACTERS_DIR

    namepath = f"{CHARACTERS_DIR}/nora/norm"
    with open(f"{namepath}/magic.json", "r") as magic_fl, open(
        f"{namepath}/taunts.json", "r"
    ) as taunts_fl:
        magic_info = json.load(magic_fl)
        taunts = json.load(taunts_fl)

    norm = Character(
        name="Norm",
        bio="It's a long story, to be honest.",
        magic_info=magic_info,
        taunts=taunts,
    )
    return norm
