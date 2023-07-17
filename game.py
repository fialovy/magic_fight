import json
import os
import random
import time

from character import Character
from game_macros import CHARACTERS_DIR, OPPONENT_SPECIAL_ABILITY_CHANCE
from game_macros import SpellChoice, SpecialChoice
from special_abilities import SpecialAbility

from typing import Any, Callable, Optional


class Game:
    all_characters: dict[str, Character] = {}
    player: Character
    opponent: Character

    def __init__(self) -> None:
        self.set_up_characters()

    def set_up_characters(self) -> None:
        for name in os.listdir(f"{CHARACTERS_DIR}"):
            character = Character(name=name.title())
            self.all_characters[name] = character

    def get_input_choice(
        self,
        prompt: str,
        choices: dict[str, Any],
        capitalize_choice: bool = True,
        offer_random_choice: bool = False,
    ) -> str:
        """Given a custom prompt and list of text choices, prompt user to
        make a choice, and insist that they do so correctly until a proper
        one can be returned.
        """
        input_choices = dict(enumerate(choices))
        random_choice_index = len(choices)
        if offer_random_choice:
            input_choices[random_choice_index] = "Choose for me! 🔮"

        choice = None
        while choice is None:
            print(prompt)
            for idx, item in input_choices.items():
                print(f"{idx}: {item.title() if capitalize_choice else item}\n")

            choice_input = input(">>> ")
            try:
                choice = int(choice_input.strip())
            except Exception:
                print("Please choose a number in the given range.")
                choice = None
                continue

            # ...but the enum made this 'interface' easy to validate.
            if choice not in input_choices:
                print("Please choose a number in the given range.")
                choice = None

        if choice == random_choice_index and offer_random_choice:
            del input_choices[random_choice_index]
            return random.choice(list(input_choices.values()))

        return input_choices[choice]

    def confirm_input_choice(
        self,
        choice: str | int,
        prompt: str,
        deny_func: Callable,
        deny_func_kwargs: Optional[dict[str, Any]] = None,
    ) -> str:
        """Print prompt presumably associated with some choice
        (e.g., info about a chosen character), and ask for y/n confirmation.

        Call given deny_func to custom 'reset' if they do not confirm.
        """
        deny_func_kwargs = deny_func_kwargs or {}
        confirmed_choice = None

        while confirmed_choice is None:
            print(prompt)
            print(f"Confirm choice? Type y or n.")

            confirm = input(">>> ")
            try:
                confirm = confirm.strip().lower()
            except Exception:
                print('Please type "y" or "n"')
                continue

            if confirm == "y":
                confirmed_choice = choice
            elif confirm == "n":
                return deny_func(**deny_func_kwargs)
            else:
                print('Please type "y" or "n"')
                continue

        return confirmed_choice

    def select_character(
        self, prompt: str = "Press a key to choose a character: \n"
    ) -> str:
        chosen_input = self.get_input_choice(
            prompt=prompt,
            choices=self.all_characters,
            capitalize_choice=True,
            offer_random_choice=True,
        )
        chosen_confirmed = self.confirm_input_choice(
            choice=chosen_input,
            prompt=f"{self.all_characters[chosen_input].ascii_art}\n\n{self.all_characters[chosen_input].bio}\n",
            deny_func=self.select_character,
            deny_func_kwargs={"prompt": prompt},
        )

        return chosen_confirmed

    def _construct_player_spell_choices(self) -> dict[str, SpellChoice | SpecialChoice]:
        """During a player's turn, construct a varying list of spell choices
        based on what is available in the character JSON.

        Return dict that is still useful to us in terms of hits.
        """
        choices: dict[str, SpellChoice | SpecialChoice] = {}

        for dimension, info in self.player.magic_info["deals"].items():
            # Not everyone can do every kind of magic, which means they
            # might be better at fewer things.
            if not info["spells"]:
                continue
            # Rotate among the available spells for each dimension
            choice_key = f'{random.choice(info["spells"])} ({dimension})'
            choices[choice_key] = SpellChoice(dimension=dimension, hit=info["amount"])

        for ability_name, info in self.player.special_abilities_info.items():
            choices[ability_name] = SpecialChoice(
                description=info["description"], effect=info["effect"]
            )

        return choices

    def hit(self, whom: Character, dimension: str, max_hit: int) -> None:
        """Hit character (player or opponent) with up to the amount of given
        dimension's magic they take.
        """
        hit = min(whom.magic_info["takes"][dimension]["amount"], max_hit)
        whom.life -= hit
        print(f"{whom.name} takes {hit} {dimension} damage!\n")
        time.sleep(1)

    def player_turn(self) -> None:
        spell_infos = self._construct_player_spell_choices()
        spell = self.get_input_choice(
            prompt="Choose your spell:\n", choices=spell_infos, capitalize_choice=False
        )
        choice = spell_infos[spell]

        if isinstance(choice, SpellChoice):
            dimension, max_hit = choice.dimension, choice.hit
            self.hit(self.opponent, dimension, max_hit)
            self.opponent.possibly_react()

        if isinstance(choice, SpecialChoice):
            description, effect = choice.description, choice.effect
            self.confirm_input_choice(
                choice=spell,
                prompt=description,
                deny_func=self.player_turn,
            )
            ability = SpecialAbility(
                player=self.player, opponent=self.opponent, effect=choice.effect
            )
            self.player, self.opponent = ability.perform()

    def opponent_turn(self) -> None:
        self.opponent.possibly_taunt()

        # the opponent of the opponent is of course the player, so keep that
        # in mind when returning player, opponent result format
        (
            modified_opponent_as_player,
            modified_player_as_opponent,
        ) = self.opponent.possibly_activate_special_ability(
            chance=OPPONENT_SPECIAL_ABILITY_CHANCE,
            human_opponent=self.player,
        )
        self.opponent, self.player = (
            modified_opponent_as_player,
            modified_player_as_opponent,
        )

        spell_info = self.opponent.magic_info["deals"]
        # Recall that not everyone can deal every kind, as a cost to being
        # super strong in some.
        able_dimensions = [dim for dim, info in spell_info.items() if info["spells"]]
        dimension = random.choice(able_dimensions)
        spell = random.choice(spell_info[dimension]["spells"])

        print(f'{self.opponent.name} chooses: "{spell}"')
        time.sleep(1)
        self.hit(self.player, dimension, max_hit=spell_info[dimension]["amount"])

    def play(self) -> None:
        player_choice = self.select_character()
        self.player = self.all_characters[player_choice]
        # You cannot be your own opponent (not even you, Adrian).
        del self.all_characters[player_choice]

        opponent_choice = self.select_character(
            prompt="Press a key to choose your opponent: \n"
        )
        self.opponent = self.all_characters[opponent_choice]

        print(f"\n{self.opponent.name} is ready to duel!\n")
        time.sleep(1)
        print("Ready?\n")
        time.sleep(2)

        # well it is a start
        while True:
            self.player.print_life()
            self.opponent.print_life()
            time.sleep(1)

            self.player_turn()
            if self.opponent.life <= 0:
                print(
                    f"You have defeated {self.opponent.name}! Congratulations, Sorcerer."
                )
                time.sleep(2)
                return

            self.opponent_turn()
            if self.player.life <= 0:
                print(f"{self.opponent.name} has bested you. Game over.")
                time.sleep(2)
                return
