import json
import os
import re


CHARACTERS_DIR = 'character_infos'


class Character:

    def __init__(self, name, bio, magic_info, taunts):
        self.name = name
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
        for name in os.listdir(f'{CHARACTERS_DIR}'):
            namepath = f'{CHARACTERS_DIR}/{name}'

            with open(f'{namepath}/bio.txt', 'r') as bio_fl, \
                 open(f'{namepath}/magic.json', 'r') as magic_fl, \
                 open(f'{namepath}/taunts.json', 'r') as taunts_fl:
                self.opponents[name] = Character(
                    name = name,
                    bio = bio_fl.read().strip(),
                    magic_info = json.load(magic_fl),
                    taunts = json.load(taunts_fl)
                )

    def select_character(self):
        chosen = False

        while not chosen:
            print('Press a key to choose a character:')
            choice = input('>>> ')
            try:
                choice = int(choice.strip())
                chosen = True
            except:
                print('Please choose a number in the given range.')

    def play(self):
        self.select_character()

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
