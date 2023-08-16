# magic_fight

### wat?

Very simple text loop game. Cast a spell!

For the love of gods, make sure it's Python 3+ (preferably 3.10+). Then:

`pip install -r requirements.txt`

`python magic_fight.py`

I originally wanted to make it jUsT wOrK with no dependencies whatsoever (and
made a dumb workaround for the upsidedown library for that very reason), but the allure
of mypy was far too strong.

So, sorry. There's a requirements file of the perfectly primitive sort. 🤪

### Recommendation

`alias myblackisort='black .; isort .; mypy .;'`

### How to Submit a Character

To create a new character, you must create a new subdirectory within the `characters/`
directory with the name of your choice. During gameplay, the character's name will
be nicely title-cased and formatted. For example:

`vasily` becomes `Vasily`

`mary_anne` becomes `Mary Anne`

Next, you must add the two required files within your new character directory:

1. `bio.txt` - A short description of the character. I don't throw it to OpenAI or anything
yet, so don't get too excited. It's just to show a nice prompt when you choose a character
at the beginning.
2. `magic.json` - A JSON file containing your character's spell information. It should
be structured like:

<TODO>

![Character doodles](images/neat.png)
