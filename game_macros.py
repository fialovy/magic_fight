import random
from typing import Final

CHARACTERS_DIR: Final = "characters"
GAME_LIFE: Final = 20
OPPONENT_SPECIAL_ABILITY_CHANCE: Final = 0.2


def did_it_happen(chance: float = 0.5) -> bool:
    """Helper for all kinds of things that occur at a given chance between
    0 and 1.
    """
    return 100 * chance > random.randint(0, 100)
