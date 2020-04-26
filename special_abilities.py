"""
Special abilities to load from one spot.
"""
import json
import time

from game_macros import did_it_happen


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


def _potion_life_effect():
    """Return a positive or negative integer value to add to poor,
    drunken Winston's current life value.
    """
    sign = -1 if did_it_happen(0.5) else 1
    return sign * random.choice(range(1, 6))


def potionify(winston):
    from character import Character

    effect = _potion_life_effect()
    winston.life += effect

    drunk_winston = Character(name="Winston")
    drunk_winston.life = winston.life
    #drunk_winston.magic/special abilities = ...

    positive_effect = effect > 0
    condrunktion = "and" if positive_effect else "but"
    action = "gives him" if positive_effect else ""
    # TODO: make comments to choose from for this, too.
    commentary = "That's some good stuff" if positive_effect else "Poor Winston."
    print(
        f"Winston gets drunk, {condrunktion} this time it {action} "
        f"{abs(effect)} life points! {commentary}."
    )
    time.sleep(1)

    return drunk_winston
