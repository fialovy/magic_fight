import json
import os
import random
import time

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

    def _construct_player_spell_choices(self):
        """For better or ugly, conform to le input helper...

        Return dict that is still useful to us in terms of hits.
        """
        choices = {}

        for dimension, info in self.player.magic_info['deals'].items():
            # Not everyone can do every kind of magic, which means they
            # might be better at fewer things.
            if not info['spells']:
                continue
            choice_key = f'{random.choice(info["spells"])} ({dimension})'
            choices[choice_key] = (dimension, info['amount'])

        return choices

    def hit(self, whom, dimension, max_hit):
        """Hit opponent with up to the amount of given dimension's magic they take."""
        hit = min(
            whom.magic_info['takes'][dimension]['amount'],
            max_hit
        )
        whom.life -= hit
        print(f'{whom.name} takes {hit} {dimension} damage!\n')  # TODO: changing words here
        time.sleep(1)

    def player_turn(self):
        spell_infos = self._construct_player_spell_choices()
        spell = self.attempt_input_choice(
            prompt='Choose your spell:\n',
            choices=spell_infos,
            capitalize_choice=False
        )
        dimension, max_hit = spell_infos[spell]
        self.hit(self.opponent, dimension, max_hit)

    def opponent_turn(self):
        self.opponent.possibly_taunt()

        spell_info = self.opponent.magic_info['deals']
        dimension = random.choice(list(spell_info.keys()))
        spell = random.choice(spell_info[dimension]['spells'])

        print(f'{self.opponent} chooses to {spell}')
        time.sleep(1)
        self.hit(self.player, dimension, max_hit=spell_info[dimension]['amount'])

    def play(self):
        chosen = self.select_character()
        self.player = self.opponents[chosen]
        # You cannot be your own opponent (not even you, Adrian).
        del self.opponents[chosen]

        self.opponent = random.choice(list(self.opponents.values()))
        print(f'\n{self.opponent.name} wants to duel!\n')
        time.sleep(1)
        print('Ready?\n')
        time.sleep(2)

        # well it is a start
        while self.player.life > 0 and self.opponent.life > 0:
            print(f'{self.player.name}: {"+"*self.player.life}')
            print(f'{self.opponent.name}: {"+"*self.opponent.life}\n')
            time.sleep(1)
            self.player_turn()
            self.opponent_turn()

        if self.player.life < 0:
            print(f'{self.opponent.name} has bested you. Game over.')
            time.sleep(2)
        else:
            print(f'You have defeated {self.opponent}! Congratulations, Sorcerer.')
            time.sleep(2)

        return
