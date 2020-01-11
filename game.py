import json
import os
import random
import re

from character import Character


CHARACTERS_DIR = 'character_infos'


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
                    name = name.title(),
                    bio = bio_fl.read().strip(),
                    magic_info = json.load(magic_fl),
                    taunts = json.load(taunts_fl)
                )

    def attempt_input_choice(self, prompt, choices, capitalize_choice=True):
        """Given a custom prompt and list of text choices, prompt user to
        make a choice, and insist that they do so correctly until a proper
        one can be returned.
        """
        print(prompt)

        choices = dict(enumerate(choices))
        for idx, item in choices.items():
            print(f'{idx}: {item.title() if capitalize_choice else item}\n')

        choice = input('>>> ')
        try:
            choice = int(choice.strip())
        except:
            print('Please choose a number in the given range.')
            self.attempt_input_choice(prompt, choices, capitalize_choice)

        # ...but the enum made this 'interface' easy to validate.
        if choice not in choices:
            print('Please choose a number in the given range.')
            self.attempt_input_choice(prompt, choices, capitalize_choice)
        else:
            # Name key of chosen character
            return choices[choice]

    def select_character(self):

        def _confirm_character(name):
            print(f'{self.opponents[name].bio}\n')
            print(f'Confirm choice? Type y or n.')

            confirm = input('>>> ')
            try:
                confirm = confirm.strip().lower()
            except:
                print('Please type "y" or "n"')
                _confirm_character(name)

            if confirm == 'y':
                return name
            elif confirm == 'n':
                return self.select_character()
            else:
                print('Please type "y" or "n"')
                _confirm_character(name)

        chosen = self.attempt_input_choice(
            prompt='Press a key to choose a character:\n',
            choices=self.opponents,
            capitalize_choice=True
        )
        chosen = _confirm_character(chosen)

        return chosen

    def opponent_turn(self):
        pass

    def _construct_player_spell_choices(self):
        """For better or ugly, conform to le input helper..."""
        choices = {}

        for dimension, info in self.player.magic_info['deals'].items():
            # Not everyone can do every kind of magic, which means they
            # might be better at fewer things.
            if not info['spells']:
                continue
            choice_key = f'{random.choice(info["spells"])} ({dimension})'
            choices[choice_key] = (dimension, info['amount'])

        return choices

    def hit_opponent(self, dimension, max_hit):
        """Hit opponent with up to the amount of given dimension's magic they take."""
        hit = min(
            self.opponent.magic_info['takes'][dimension]['amount'],
            max_hit
        )
        self.opponent.life -= hit
        print(f'{self.opponent.name} takes {hit} {dimension} damage!\n')  # TODO: changing words here

    def player_turn(self):
        spell_infos = self._construct_player_spell_choices()
        spell = self.attempt_input_choice(
            prompt='Choose your spell:\n',
            choices=spell_infos,
            capitalize_choice=False
        )
        dimension, max_hit = spell_infos[spell]
        self.hit_opponent(dimension, max_hit)

    def play(self):
        chosen = self.select_character()
        self.player = self.opponents[chosen]
        # You cannot be your own opponent (not even you, Adrian).
        del self.opponents[chosen]

        self.opponent = random.choice(list(self.opponents.values()))
        print(f'\n{self.opponent.name} wants to duel!\n')
        print('Ready?\n')

        # well it is a start
        while self.player.life > 0 and self.opponent.life > 0:
            print(f'{self.player.name}: {"+"*self.player.life}')
            print(f'{self.opponent.name}: {"+"*self.opponent.life}\n')
            self.player_turn()
            self.opponent_turn()

        print(f'A prompt about how you either won or lost the game.')
        return
