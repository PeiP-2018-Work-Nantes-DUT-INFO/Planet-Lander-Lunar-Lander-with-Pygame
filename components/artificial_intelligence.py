class ArtificialIntelligence(object):
    def __init__(self):
        self.landing = None
        self.aircraft = None
        pass

    def game_start(self, landing, aircraft):
        self.landing = landing
        self.aircraft = aircraft

    def changed_state(self):
        pass

    def get_next_command(self, now):
        pass

    def game_over(self):
        pass

    def loose(self):
        pass

    def win(self):
        pass
