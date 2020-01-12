import random
import time


class Character:

    def __init__(self, name, bio, magic_info, taunts):
        self.name = name
        self.bio = bio
        self.magic_info = magic_info
        self.taunts = taunts
        self.life = 10

    def possibly_taunt(self):
        """Depending on their percent chance of doing so (some characters
        are nicer), pick and say a random taunt.
        """
        if 100 * self.taunts['chance'] > random.randint(0,100):
            print(f'{self.name} says: {random.choice(self.taunts["taunts"])}\n')
            time.sleep(1)
