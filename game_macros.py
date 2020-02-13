CHARACTERS_DIR = "characters"
GAME_LIFE = 20
OPPONENT_SPECIAL_ABILITY_CHANCE = 0.2

from collections import namedtuple

SpellChoice = namedtuple("SpellChoice", ["dimension", "hit"])
SpecialChoice = namedtuple("SpecialChoice", ["description", "effect"])
