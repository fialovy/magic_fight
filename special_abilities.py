import json
import time


# Special abilities to load from one spot.


def change_to_norm(nora):
    # Circular imports are an unfortunate thing...
    from character import Character
    from game import CHARACTERS_DIR

    nora.life -= 1

    norm_namepath = f"{CHARACTERS_DIR}/nora/norm"
    norm = Character(name="Norm", special_namepath=norm_namepath)
    norm.life = nora.life

    print("Nora becomes Norm!")
    time.sleep(1)

    return norm


def change_to_nora(norm):
    from character import Character

    norm.life -= 1

    # Re-instantiate because why not. Only life changes.
    nora = Character(name="Nora")
    nora.life = norm.life

    print("Norm becomes Nora!")
    time.sleep(1)

    return nora
