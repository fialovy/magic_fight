import json
import os
import random
import time

import special_abilities

from game_macros import CHARACTERS_DIR, GAME_LIFE

class Character:
    def __init__(self, name, bio, magic_info, taunts):
        self.name = name
        self.bio = bio
        self.magic_info = magic_info
        self.taunts = taunts
        self.life = GAME_LIFE

        self.set_special_abilities()

    def set_special_abilities(self):
        self.special_abilities_info = {}

        namepath = f"{CHARACTERS_DIR}/{self.name.lower()}"
        special_path = f"{namepath}/special.json"
        # Boo hoo; not everyone has special abilities right now.
        if os.path.exists(special_path):
            with open(special_path, "r") as special_fl:
                special_abilities_info = json.load(special_fl)
            self.special_abilities_info = special_abilities_info

    def possibly_taunt(self):
        """Depending on their percent chance of doing so (some characters
        are nicer), pick and say a random taunt.
        """
        if 100 * self.taunts["chance"] > random.randint(0, 100):
            print(f'{self.name} says: {random.choice(self.taunts["taunts"])}\n')
            time.sleep(1)

    def possibly_activate_special_ability(self, chance):
        """Depending on percent chance, possibly auto-activiate a special ability.

        Definitely meant for computer opponents at the moment.

        Chance is hard-coded for this now because I am sad.
        """
        if 100 * chance > random.randint(0, 100):
            abilities = [
                ability["effect"] for ability in self.special_abilities_info.values()
            ]

            if not abilities:
                return

            ability = random.choice(abilities)
            ability_func = getattr(special_abilities, ability)

            return ability_func(self)
