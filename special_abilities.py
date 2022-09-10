import copy
import json
import random
import sys
import time
import upsidedown

from character import Character
from game_macros import did_it_happen



class SpecialAbility:
    # TODO: fix this class; it seems contrived
    def __init__(self, player, opponent, effect):
        self.player = player
        self.opponent = opponent
        self.effect_func = getattr(sys.modules[__name__], effect)

    def perform(self, **kwargs):
        import pdb; pdb.set_trace()  
        return self.effect_func(self.player, self.opponent, **kwargs)

# Just a mess of special abilities to load from one spot. For now they
# get associated to their characters via the spell choices, which
# opens the potential for sharing (that or I am too lazy to just put
# these into the character modules nicely)

def change_to_norm(nora, *_, **__):
    # Circular imports are an unfortunate thing...
    from game import CHARACTERS_DIR

    nora.life -= 1

    norm_namepath = f"{CHARACTERS_DIR}/nora/norm"
    norm = Character(name="Norm", special_namepath=norm_namepath)
    norm.life = nora.life

    print(f"{nora.name} becomes Norm!")
    time.sleep(1)

    return norm


def change_to_nora(norm, *_, **__):
    norm.life -= 1

    # Re-instantiate because why not. Only life changes.
    nora = Character(name="Nora")
    nora.life = norm.life

    print(f"{norm.name} becomes Nora!")
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

    commentary = (
        "That's some good stuff" if positive_effect else f"Poor {character_name}."
    )
    print(
        f"{character_name} gets drunk, {condrunktion} this time it {action} "
        f"{abs(effect)} life points! {commentary}."
    )
    time.sleep(1)


def potionify(player, *_, **__):
    effect = _potion_life_effect()
    player.life += effect

    drunkard = Character(name=player.name)
    drunkard.life = player.life
    drunkard.magic_info = _drunkify_spells(drunkard.magic_info)
    drunkard._set_special_abilities(f"{drunkard.namepath}/drunk_special.json")
    _print_potion_effect(drunkard.name, effect)

    return drunkard


def attempt_sobering(player, *_, is_computer=False):
    """was it a good idea?"""
    if did_it_happen():
        # Restore defaults!
        sober = Character(name=player.name)
        sober.life = player.life + 1

        if not is_computer:
            print("\nIt worked! You have magically sobered up and gained 1 life point!")
        else:
            print(f"\n{player.name} has sobered up and gained 1 life point!")
        time.sleep(1)

        return sober
    else:
        player.life -= 1
        if not is_computer:
            print(
                f"\nThere is no shortcut to sobriety, {player.name}. But this crappy "
                f"concoction did manage to take a life point from you."
            )
        else:
            print(
                f"\n{player.name} is learning the hard way that there is no "
                f"shortcut to sobriety. They lose 1 life point!"
            )
        time.sleep(1)
        return player


def orbs_of_disorderify(player, opponent, **__):
    print("coming soon! winfield's orbs need some maintenance...")
    return player
