import copy
import json
import random
import sys
import time
import upsidedown

from character import Character
from game_macros import did_it_happen, SpecialEffect


class SpecialAbility:
    def __init__(self, player, opponent, effect):
        self.player = player
        self.opponent = opponent
        # literally just load them all from here for now
        self.effect_func = getattr(sys.modules[__name__], effect)

    def perform(self, **additional_options):
        return self.effect_func(self.player, self.opponent, **additional_options)


def change_to_norm(player, opponent, **_):
    # Circular imports are an unfortunate thing...
    from game import CHARACTERS_DIR

    player.life -= 1

    norm_namepath = f"{CHARACTERS_DIR}/nora/norm"
    norm = Character(name="Norm", special_namepath=norm_namepath)
    norm.life = player.life

    print(f"{player.name} becomes Norm!")
    time.sleep(1)

    return norm, opponent


def change_to_nora(player, opponent, **_):
    player.life -= 1

    # Re-instantiate because why not. Only life changes.
    nora = Character(name="Nora")
    nora.life = player.life

    print(f"{player.name} becomes Nora!")
    time.sleep(1)

    return nora, opponent


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


def potionify(player, opponent, **_):
    effect = _potion_life_effect()
    player.life += effect

    drunkard = Character(name=player.name)
    drunkard.life = player.life
    # TODO: don't deepcopy
    drunkard.magic_info = _drunkify_spells(drunkard.magic_info)
    drunkard._set_special_abilities(f"{drunkard.namepath}/drunk_special.json")
    _print_potion_effect(drunkard.name, effect)

    return drunkard, opponent


def attempt_sobering(player, opponent, is_computer=False):
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
        return player, opponent


def orbs_of_disorderify(player, opponent, **_):
    """
    Mix up the hit values of the opponent's spells.
    """
    deal_amounts = [dim['amount'] for dim in opponent.magic_info['deals'].values()]

    for dimension_info in opponent.magic_info["deals"].values():
        now_deals = deal_amounts.pop(random.randrange(len(deal_amounts)))
        dimension_info["amount"] = now_deals

    return player, opponent
