import json
import os
import random
import time

from game_macros import CHARACTERS_DIR, GAME_LIFE, did_it_happen


class Character:
    def __init__(self, name, special_namepath=None):
        self.life = GAME_LIFE
        self.name = name
        self.namepath = special_namepath or f"{CHARACTERS_DIR}/{name.lower()}"

        self._set_bio()
        self._set_magic_info()
        self._set_taunts()
        self._set_reactions()
        self._set_special_abilities()

    def _set_bio(self):
        with open(f"{self.namepath}/bio.txt", "r") as bio_fl:
            self.bio = bio_fl.read().strip()

    def _set_magic_info(self):
        with open(f"{self.namepath}/magic.json", "r") as magic_fl:
            self.magic_info = json.load(magic_fl)

    def _set_taunts(self):
        with open(f"{self.namepath}/taunts.json", "r") as taunts_fl:
            self.taunts = json.load(taunts_fl)

    def _set_reactions(self):
        reactions_path = f"{self.namepath}/reactions.json"
        if os.path.exists(reactions_path):
            with open(reactions_path, "r") as reactions_fl:
                self.reactions = json.load(reactions_fl)
        else:
            self.reactions = None

    def _set_special_abilities(self, special_path=None):
        self.special_abilities_info = {}

        special_path = special_path or f"{self.namepath}/special.json"
        # Boo hoo; not everyone has special abilities right now.
        if os.path.exists(special_path):
            with open(special_path, "r") as special_fl:
                special_abilities_info = json.load(special_fl)
            self.special_abilities_info = special_abilities_info

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
