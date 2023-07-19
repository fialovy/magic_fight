import json
import os
import random
import time
from typing import Any, Optional, TypedDict

from game_macros import (CHARACTERS_DIR, GAME_LIFE, CharacterMagicInfo,
                         CharacterReactions, CharacterSpecialAbilitiesInfo,
                         CharacterTaunts, SpecialChoice, SpellChoice,
                         did_it_happen)


class Character:
    life: int  # amount of juice left
    name: str
    namepath: str  # how to get to the files (because shapeshifters)
    bio: str  # a short description of the character
    ascii_art: str  # this game has ✨ advanced graphics ✨
    magic_info: CharacterMagicInfo
    taunts: Optional[CharacterTaunts]
    reactions: Optional[CharacterReactions]
    special_abilities_info: dict[str, CharacterSpecialAbilitiesInfo]

    def __init__(self, name: str, special_namepath: Optional[str] = None) -> None:
        self.life = GAME_LIFE
        self.name = name
        self.namepath = special_namepath or f"{CHARACTERS_DIR}/{name.lower()}"

        self._set_bio()
        self._set_ascii_art()
        self._set_magic_info()
        self._set_taunts()
        self._set_reactions()
        self._set_special_abilities()

    def _set_attr_from_file(
        self,
        attr: str,
        filepath: str,
        strip: Optional[bool] = False,
        allow_empty: Optional[bool] = False,
        empty_val: Optional[Any] = None,
    ) -> None:
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

    def _set_bio(self) -> None:
        self._set_attr_from_file(
            attr="bio",
            filepath=f"{self.namepath}/bio.txt",
            strip=True,
        )

    def _set_ascii_art(self) -> None:
        self._set_attr_from_file(
            attr="ascii_art",
            filepath=f"{self.namepath}/ascii_art.txt",
            strip=True,
            allow_empty=True,
            empty_val="",
        )

    def _set_magic_info(self) -> None:
        self._set_attr_from_file(
            attr="magic_info",
            filepath=f"{self.namepath}/magic.json",
        )

    def _set_taunts(self) -> None:
        self._set_attr_from_file(
            attr="taunts",
            filepath=f"{self.namepath}/taunts.json",
            allow_empty=True,
            empty_val=None,
        )

    def _set_reactions(self) -> None:
        self._set_attr_from_file(
            attr="reactions",
            filepath=f"{self.namepath}/reactions.json",
            allow_empty=True,
            empty_val=None,
        )

    def _set_special_abilities(self, special_path: Optional[str] = None) -> None:
        self._set_attr_from_file(
            attr="special_abilities_info",
            filepath=special_path or f"{self.namepath}/special.json",
            allow_empty=True,
            empty_val={},
        )

    def print_life(self) -> None:
        print(f'{self.name}: {"+"*self.life}({self.life} sparks left)')

    def possibly_taunt(self) -> None:
        """Depending on their percent chance of doing so and whether they actually have taunts,
        (some characters are nicer), pick and say a random taunt.
        """
        if self.taunts is not None and did_it_happen(self.taunts["chance"]):
            print(f'{self.name} says: {random.choice(self.taunts["taunts"])}\n')
            time.sleep(1)

    def possibly_react(self) -> None:
        """If character can verbally react to a hit (some are more vocal),
        do so based on their chance.
        """
        if self.reactions is not None and did_it_happen(self.reactions["chance"]):
            print(
                f"{self.name} says: " f'{random.choice(self.reactions["reactions"])}\n'
            )
            time.sleep(1)
