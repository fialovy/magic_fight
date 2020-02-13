import json
import time


# Special abilities to load from one spot.


def change_to_norm(nora):
    # Circular imports are an unfortunate thing...
    from character import Character
    from game import CHARACTERS_DIR

    # Gross, I know, but I also don't want the opponent to do this
    # extra times.
    if nora.name == "Norm":
        return

    nora.life -= 1

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
    norm.life = nora.life

    print("Nora becomes Norm!")
    time.sleep(1)

    return norm


def change_to_nora(norm):
    # Gross, I know, but I also don't want the opponent to do this
    # extra times.
    if norm.name == "Nora":
        return

    norm.life -= 1
    breakpoint() 
    nora.life = norm.life

    print("Norm becomes Nora!")
    time.sleep(1)

    return nora
