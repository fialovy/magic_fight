from game import Game


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
        \n
        """
    )
    game = Game()
    game.play()


if __name__ == "__main__":
    main()
