import json
import os
import re


class Character:

    def __init__(self, bio, magic_info, taunts):
        self.bio = bio
        self.magic_info = magic_info
        self.taunts = taunts
        self.life = 10

class Game:

    opponents = {}
    player = None

    def __init__(self):
        self.set_up_characters()

    def set_up_characters(self):
        # Better to just read JSONs or something? Yeah, well sue me.
        for name in os.listdir(os.path.abspath('character_infos')):
            import pdb; pdb.set_trace() 
            opponents[name] = Character(bio, magic_info, taunts)

    def play(self):
        print("Press a key to choose a character!:")


def main():
    print("""Welcome to Magic Fight!

        Choose your sorcerer, figure out their strengths and weaknesses,
        and try to figure out how to beat everyone else!

        Any fighter - including you - loses if they take 10 units of damage.
        Different kinds of magic affect the characters in different ways, so
        pay attention.

        What kinds of magic, you ask? There are 6: dark, light, chaotic,
        ordered, hot, and cold.

        A character can likewise deal damage from one of the 6 kinds at a time.
        What kinds, and how much? You have to figure that out, too. Good luck!
        \n\n
        """
    )
    game = Game()
    game.play()

if __name__ == "__main__":
    main()
