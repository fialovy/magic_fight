import json
import os
import random
import time

from typing import Optional, TypedDict

from game_macros import CHARACTERS_DIR, GAME_LIFE, did_it_happen


# Some characters say taunts. If so, they have a likelihood of doing so each
# round (between 0 and 1), plus a list of choice things to say when they do.
CharacterTaunts = TypedDict("CharacterTaunts", {"chance": float, "taunts": list[str]})
# Same idea as above, but when you hit them.
CharacterReactions = TypedDict(
    "CharacterReactions", {"chance": float, "reactions": list[str]}
)
# 'effect' must be the name of a function that will be loaded when used
CharacterSpecialAbilitiesInfo = TypedDict(
    "CharacterSpecialAbilitiesInfo", {"description": str, "effect": str}
)


class Character:
    life: int  # amount of juice left
    name: str
    namepath: str  # how to get to the files (because shapeshifters)
    bio: str  # a short description of the character
    ascii: str  # ascii art because this game has ✨ advanced graphics ✨
    magic_info: dict  # too nested; i aint typin this
    taunts: Optional[CharacterTaunts]
    reactions: Optional[CharacterReactions]
    special_abilities_info: dict[str, CharacterSpecialAbilitiesInfo]

    def __init__(self, name: str, special_namepath: Optional[str] = None):
        self.life = GAME_LIFE
        self.name = name
        self.namepath = special_namepath or f"{CHARACTERS_DIR}/{name.lower()}"

        self._set_bio()
        self._set_ascii()
        self._set_magic_info()
        self._set_taunts()
        self._set_reactions()
        self._set_special_abilities()

    def _set_attr_from_file(
        self, attr, filepath, strip=False, allow_empty=False, empty_val=None
    ):
        """
        Read and set character data from a file, and set the character attribute
        to empty_val if file does not exist.

        Expected file types for now include txt and json. Maybe we can use actual
        typing at some point.

        If strip is true, well...do strip() to get rid of whitespace on the ends.
        """
        if os.path.exists(filepath):
            with open(filepath, "r") as attr_fl:
                if filepath.endswith("txt"):
                    val = attr_fl.read()
                    if strip:
                        val = val.strip()
                elif filepath.endswith("json"):
                    val = json.load(attr_fl)
                else:
                    raise ValueError(f"Unsupported filetype at the moment: {filepath}")
            setattr(self, attr, val)
        elif allow_empty:
            setattr(self, attr, empty_val)
        else:
            raise FileNotFoundError(
                f"Could not set {attr}! Expected file not found: {filepath}"
            )

    def _set_bio(self):
        self._set_attr_from_file(
            attr="bio",
            filepath=f"{self.namepath}/bio.txt",
            strip=True,
        )

    def _set_ascii(self):
        self._set_attr_from_file(
            attr="ascii",
            filepath=f"{self.namepath}/ascii_art.txt",
            strip=True,
            allow_empty=True,
            empty_val="",
        )

    def _set_magic_info(self):
        self._set_attr_from_file(
            attr="magic_info",
            filepath=f"{self.namepath}/magic.json",
        )

    def _set_taunts(self):
        self._set_attr_from_file(
            attr="taunts",
            filepath=f"{self.namepath}/taunts.json",
        )

    def _set_reactions(self):
        self._set_attr_from_file(
            attr="reactions",
            filepath=f"{self.namepath}/reactions.json",
            allow_empty=True,
            empty_val=None,
        )

    def _set_special_abilities(self, special_path=None):
        self._set_attr_from_file(
            attr="special_abilities_info",
            filepath=f"{self.namepath}/special.json",
            allow_empty=True,
            empty_val={},
        )

    def possibly_taunt(self):
        """Depending on their percent chance of doing so (some characters
        are nicer), pick and say a random taunt.
        """
        if did_it_happen(self.taunts["chance"]):
            print(f'{self.name} says: {random.choice(self.taunts["taunts"])}\n')
            time.sleep(1)

    def possibly_react(self):
        """If character can verbally react to a hit (some are more vocal),
        do so based on their chance.
        """
        if self.reactions is not None and did_it_happen(self.reactions["chance"]):
            print(
                f"{self.name} says: " f'{random.choice(self.reactions["reactions"])}\n'
            )
            time.sleep(1)

    def possibly_activate_special_ability(self, chance):
        """Depending on percent chance, possibly auto-activiate a special ability.

        Definitely meant for computer opponents at the moment.

        Chance is hard-coded for this now because I am sad.
        """
        if did_it_happen(chance):
            import special_abilities

            abilities = [
                ability["effect"] for ability in self.special_abilities_info.values()
            ]

            if not abilities:
                return

            ability = random.choice(abilities)
            ability_func = getattr(special_abilities, ability)

            return ability_func(self)
