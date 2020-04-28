"""
Special abilities to load from one spot.
"""
import copy
import json
import random
import time
import upsidedown

from character import Character
from game_macros import did_it_happen


def change_to_norm(nora):
    # Circular imports are an unfortunate thing...
    from game import CHARACTERS_DIR

    nora.life -= 1

    norm_namepath = f"{CHARACTERS_DIR}/nora/norm"
    norm = Character(name="Norm", special_namepath=norm_namepath)
    norm.life = nora.life

    print("Nora becomes Norm!")
    time.sleep(1)

    return norm


def change_to_nora(norm):
    norm.life -= 1

    # Re-instantiate because why not. Only life changes.
    nora = Character(name="Nora")
    nora.life = norm.life

    print("Norm becomes Nora!")
    time.sleep(1)

    return nora


def _potion_life_effect():
    """Return a positive or negative integer value to add to poor,
    drunken character's current life value.
    """
    sign = -1 if did_it_happen() else 1
    return sign * random.choice(range(1, 6))


def _drunkify_spells(magic_info):
    """Flip the given spell descriptions upside down, because we are drunk."""
    drunken_magic = copy.deepcopy(magic_info)

    for dimension_info in drunken_magic["deals"].values():
        dimension_info["spells"] = list(
            map(upsidedown.transform, dimension_info["spells"])
        )

    return drunken_magic


def _print_potion_effect(character_name, effect):
    positive_effect = effect > 0
    condrunktion = "and" if positive_effect else "but"
    action = "gives" if positive_effect else "costs"

    # TODO: make comments to choose from for this, too.
    commentary = (
        "That's some good stuff" if positive_effect else f"Poor {character_name}."
    )
    print(
        f"{character_name} gets drunk, {condrunktion} this time it {action} "
        f"{abs(effect)} life points! {commentary}."
    )
    time.sleep(1)


def potionify(drinker):
    effect = _potion_life_effect()
    drinker.life += effect

    drunkard = Character(name=drinker.name)
    drunkard.life = drinker.life
    drunkard.magic_info = _drunkify_spells(drunkard.magic_info)
    drunkard._set_special_abilities(f"{drunkard.namepath}/drunk_special.json")
    _print_potion_effect(drunkard.name, effect)

    return drunkard


def attempt_sobering(drinker):
    """was it a good idea?"""
    if did_it_happen():
        # Restore defaults!
        sober = Character(name=drinker.name)
        sober.life = drinker.life + 1
        print("\nIt worked! You have magically sobered up and gained 1 life point!")
        time.sleep(1)

        return sober

    drinker.life -= 1
    print(
        f"\nThere is no shortcut to sobriety, {drinker.name}. But this crappy "
        f"concoction did manage to take a life point from you."
    )
    time.sleep(1)

    return drinker
