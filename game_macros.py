import random

from collections import namedtuple


CHARACTERS_DIR = "characters"
GAME_LIFE = 20
OPPONENT_SPECIAL_ABILITY_CHANCE = 0.2

SpellChoice = namedtuple("SpellChoice", ["dimension", "hit"])
SpecialChoice = namedtuple("SpecialChoice", ["description", "effect"])


def did_it_happen(chance):
    """Helper for all kinds of things that occur at a given chance between
    0 and 1.
    """
    return 100 * chance > random.randint(0, 100)
