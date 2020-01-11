class Character:

    def __init__(self, name, bio, magic_info, taunts):
        self.name = name
        self.bio = bio
        self.magic_info = magic_info
        self.taunts = taunts
        self.life = 10

    def possibly_taunt(self):
        """Depending on their chance of doing so (some characters are nicer),
        pick and say a random taunt.
        """
        import pdb; pdb.set_trace()  
