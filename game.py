import json
import os
import random
import time

from collections import namedtuple

from character import Character


CHARACTERS_DIR = 'characters'

SpellChoice = namedtuple('SpellChoice', ['dimension', 'hit'])
SpecialChoice = namedtuple('SpecialChoice', ['description', 'effect'])


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
                bio=bio_fl.read().strip()
                magic_info=json.load(magic_fl)
                taunts=json.load(taunts_fl)

            special_abilities = {}
            special_path = f'{namepath}/special.json'
            # Boo hoo; not everyone has special abilities right now.
            if os.path.exists(special_path):
                with open(special_path, 'r') as special_fl:
                    special_abilities=json.load(special_fl)

            self.opponents[name] = Character(
                name=name.title(),
                bio=bio,
                magic_info=magic_info,
                taunts=taunts,
                special_abilities=special_abilities
            )

    def get_input_choice(self, prompt, choices, capitalize_choice=True):
        """Given a custom prompt and list of text choices, prompt user to
        make a choice, and insist that they do so correctly until a proper
        one can be returned.
        """

        choices = dict(enumerate(choices))
        choice = None

        while choice is None:
            print(prompt)
            for idx, item in choices.items():
                print(f'{idx}: {item.title() if capitalize_choice else item}\n')

            choice = input('>>> ')
            try:
                choice = int(choice.strip())
            except Exception:
                print('Please choose a number in the given range.')
                choice = None
                continue

            # ...but the enum made this 'interface' easy to validate.
            if choice not in choices:
                print('Please choose a number in the given range.')
                choice = None

        # Name key of chosen character
        return choices[choice]

    def confirm_input_choice(self, choice, prompt, deny_func):
        """Print prompt presumably associated with some choice
        (e.g., info about a chosen character), and ask for y/n confirmation.

        Call given deny_func to custom 'reset' if they do not confirm.
        """
        confirmed = False

        while not confirmed:
            print(prompt)
            print(f'Confirm choice? Type y or n.')

            confirm = input('>>> ')
            try:
                confirm = confirm.strip().lower()
            except Exception:
                print('Please type "y" or "n"')
                continue

            if confirm == 'y':
                return choice
            elif confirm == 'n':
                return deny_func()
            else:
                print('Please type "y" or "n"')
                continue

    def select_character(self):

        chosen = self.get_input_choice(
            prompt='Press a key to choose a character:\n',
            choices=self.opponents,
            capitalize_choice=True
        )
        chosen = self.confirm_input_choice(
            choice=chosen,
            prompt=f'{self.opponents[chosen].bio}\n',
            deny_func=self.select_character
        )

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
            choices[choice_key] = SpellChoice(
                dimension=dimension, hit=info['amount'])

        for ability_name, info in self.player.special_abilities.items():
            choices[ability_name] = SpecialChoice(
                description=info['description'], effect=info['effect'])

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
        spell = self.get_input_choice(
            prompt='Choose your spell:\n',
            choices=spell_infos,
            capitalize_choice=False
        )
        choice = spell_infos[spell]

        if isinstance(choice, SpellChoice):
            dimension, max_hit = choice.dimension, choice.hit
            self.hit(self.opponent, dimension, max_hit)

        if isinstance(choice, SpecialChoice):
            description, effect = choice.description, choice.effect
            self.confirm_input_choice(
                choice=spell,
                prompt=description,
                deny_func=self.player_turn  # this seems wrong...
            )
            # call effect function

    def opponent_turn(self):
        self.opponent.possibly_taunt()

        spell_info = self.opponent.magic_info['deals']
        # Recall that not everyone can deal every kind, as a cost to being
        # super strong in some.
        able_dimensions = [
            dim for dim, info in spell_info.items() if info['spells']
        ]
        dimension = random.choice(able_dimensions)
        spell = random.choice(spell_info[dimension]['spells'])

        print(f'{self.opponent.name} chooses: "{spell}"')
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
        while True:
            print(f'{self.player.name}: {"+"*self.player.life}')
            print(f'{self.opponent.name}: {"+"*self.opponent.life}\n')
            time.sleep(1)

            self.player_turn()
            if self.opponent.life <= 0:
                print(f'You have defeated {self.opponent.name}! Congratulations, Sorcerer.')
                time.sleep(2)
                return

            self.opponent_turn()
            if self.player.life <= 0:
                print(f'{self.opponent.name} has bested you. Game over.')
                time.sleep(2)
                return
