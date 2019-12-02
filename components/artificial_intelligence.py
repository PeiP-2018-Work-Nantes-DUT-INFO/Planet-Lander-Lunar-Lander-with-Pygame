class ArtificialIntelligence(object):
    """
    Classe qui définie une intelligence artificielle
    """

    def __init__(self):
        self.landing = None
        self.aircraft = None
        pass

    def game_start(self, landing, aircraft):
        """Appellé à chaque début de partie"""
        self.landing = landing
        self.aircraft = aircraft

    def changed_state(self):
        """Appellé lorsque le joueur a explosé/game over"""
        pass

    def get_next_command(self, now):
        """Appelé a chaque mise à jour
        :return un tuple de taille 323 d'entier set à 0 ou à 1, ou un keycode pygame"""
        pass

    def game_over(self):
        """Appellé quand le joueur à un game_over"""
        pass

    def loose(self):
        """Appellé quand le module explose. N'appelle pas game_over"""
        pass

    def win(self):
        """Appellé quand le joueur atterit proprement sur une plateforme"""
        pass
