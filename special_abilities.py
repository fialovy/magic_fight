import copy
import json
import random
import sys
import time
from typing import Any, Optional

NO_UPSIDEDOWN = False
try:
    import upsidedown  # type: ignore
except ImportError:
    NO_UPSIDEDOWN = True

from character import Character, CharacterMagicInfo
from game_macros import CHARACTERS_DIR, did_it_happen


class SpecialAbility:
    def __init__(self, player: Character, opponent: Character, effect: str) -> None:
        self.player = player
        self.opponent = opponent
        # literally just load them all from here for now
        self.effect_func = getattr(sys.modules[__name__], effect)

    def perform(
        self, **additional_options: Optional[Any]
    ) -> tuple[Character, Character]:
        return self.effect_func(self.player, self.opponent, **additional_options)


def _shapeshift(
    player: Character,
    name: str,
    special_namepath: Optional[str] = None,
    article: Optional[str] = "",
) -> Character:
    player.life -= 1

    shapeshifted = Character(name=name, special_namepath=special_namepath)
    shapeshifted.life = player.life

    print(f"{player.name} becomes{' ' if article else ''}{article} {name}!")
    time.sleep(1)

    return shapeshifted


def change_to_norm(
    player: Character, opponent: Character, **_
) -> tuple[Character, Character]:
    norm = _shapeshift(player, "Norm", special_namepath=f"{CHARACTERS_DIR}/nora/norm")
    return norm, opponent


def change_to_nora(
    player: Character, opponent: Character, **_
) -> tuple[Character, Character]:
    nora = _shapeshift(player, "Nora")
    return nora, opponent


# TODO: if computer takes on this form, give it an easy out so it doesn't bore people
def change_to_meadow_sprite(
    player: Character, opponent: Character, **_
) -> tuple[Character, Character]:
    meadow_sprite = _shapeshift(
        player,
        "Meadow Sprite",
        special_namepath=f"{CHARACTERS_DIR}/nora/meadow_sprite",
        article="a",
    )
    return meadow_sprite, opponent


def _potion_life_effect() -> int:
    """Return a positive or negative integer value to add to poor,
    drunken character's current life value.
    """
    sign = -1 if did_it_happen() else 1
    return sign * random.choice(range(1, 6))


def _drunkify_spells(magic_info: CharacterMagicInfo) -> CharacterMagicInfo:
    """Flip the given spell descriptions upside down, because we are drunk."""
    drunken_magic = copy.deepcopy(magic_info)

    for dimension_info in drunken_magic["deals"].values():
        if not NO_UPSIDEDOWN:
            drunkified_spells = map(upsidedown.transform, dimension_info["spells"])
        else:
            drunkified_spells = map(
                lambda spell: "".join(reversed(spell)), dimension_info["spells"]
            )
        dimension_info["spells"] = list(drunkified_spells)

    return drunken_magic


def _print_potion_effect(character_name: str, effect: int) -> None:
    positive_effect = effect > 0
    condrunktion = "and" if positive_effect else "but"
    action = "gives" if positive_effect else "costs"

    commentary = (
        "That's some good stuff" if positive_effect else f"Poor {character_name}."
    )
    print(
        f"{character_name} gets drunk, {condrunktion} this time it {action} "
        f"{abs(effect)} life points! {commentary}.\n"
    )
    time.sleep(1)


def potionify(
    player: Character, opponent: Character, **_
) -> tuple[Character, Character]:
    effect = _potion_life_effect()
    player.life += effect

    drunkard = Character(name=player.name)
    drunkard.life = player.life
    # TODO: don't deepcopy
    drunkard.magic_info = _drunkify_spells(drunkard.magic_info)
    drunkard._set_special_abilities(
        special_path=f"{drunkard.namepath}/drunk_special.json"
    )
    _print_potion_effect(drunkard.name, effect)

    return drunkard, opponent


def attempt_sobering(
    player: Character, opponent: Character, is_computer: bool = False, **_
) -> tuple[Character, Character]:
    """was it a good idea?"""
    if did_it_happen():
        # Restore defaults!
        sober = Character(name=player.name)
        sober.life = player.life + 1

        if not is_computer:
            print("It worked! You have magically sobered up and gained 1 life point!\n")
        else:
            print(f"{player.name} has sobered up and gained 1 life point!\n")
        time.sleep(1)
        return sober, opponent
    else:
        player.life -= 1
        if not is_computer:
            print(
                f"There is no shortcut to sobriety, {player.name}. But this crappy "
                f"concoction did manage to take a life point from you.\n"
            )
        else:
            print(
                f"{player.name} is learning the hard way that there is no "
                f"shortcut to sobriety. They lose 1 life point!\n"
            )
        time.sleep(1)
        return player, opponent


def orbs_of_disorderify(
    player: Character, opponent: Character, is_computer: bool = False, **_
) -> tuple[Character, Character]:
    """
    Mix up the hit values of the opponent's spells.
    """
    deal_amounts = [dim["amount"] for dim in opponent.magic_info["deals"].values()]

    for dimension_info in opponent.magic_info["deals"].values():
        now_deals = deal_amounts.pop(random.randrange(len(deal_amounts)))
        dimension_info["amount"] = now_deals

    if is_computer:
        print(
            f"{player.name} has used the Orbs of Disorder to randomly "
            f"swap the hit values of your spells! Be careful! ✨🔵 ✨🟡\n"
        )

    return player, opponent
