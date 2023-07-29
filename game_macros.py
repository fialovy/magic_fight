"""
Currently the dumping ground of constants, types, and shared utils

surprise gift PR with better organization would be super welcome hehe 🫶
"""

import random
from collections import namedtuple
from typing import Any, Callable, Final, Literal, Optional, TypedDict, Union

## Constants

CHARACTERS_DIR: Final = "characters"
GAME_LIFE: Final = 15
OPPONENT_SPECIAL_ABILITY_CHANCE: Final = 0.2
DEFAULT_SPECIAL_ABILITY_TURNS = (
    3  # number of turns a special ability lasts by default, if it affects any state
)


## Types

# Some characters say taunts. If so, they have a likelihood of doing so each
# round (between 0 and 1), plus a list of choice things to say when they do.
CharacterTaunts = TypedDict("CharacterTaunts", {"chance": float, "taunts": list[str]})
# Same idea as above, but when you hit them.
CharacterReactions = TypedDict(
    "CharacterReactions", {"chance": float, "reactions": list[str]}
)
# 'effect' must be the name of a function implemented in special_abilities.py
# that will be loaded when used
CharacterSpecialAbilitiesInfo = TypedDict(
    "CharacterSpecialAbilitiesInfo", {"description": str, "effect": str}
)

SpellDimension = Literal["dark", "light", "chaotic", "ordered", "hot", "cold"]
DealsDamageInfo = TypedDict("DealsDamageInfo", {"amount": int, "spells": list[str]})
TakesDamageInfo = TypedDict("TakesDamageInfo", {"amount": int})
CharacterMagicInfo = TypedDict(
    "CharacterMagicInfo",
    {
        "deals": dict[SpellDimension, DealsDamageInfo],
        "takes": dict[SpellDimension, TakesDamageInfo],
    },
)

SpellChoice = namedtuple("SpellChoice", ["dimension", "hit"])
SpecialChoice = namedtuple("SpecialChoice", ["description", "effect"])


## General helper utils


def did_it_happen(chance: float = 0.5) -> bool:
    """Helper for all kinds of things that occur at a given chance between
    0 and 1.
    """
    return 100 * chance > random.randint(0, 100)


def get_input_choice(
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
    choice: Union[str, int],
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
