import pygame


class Temps:
    """Classe statique qui gère les temps et les durées du jeu."""

    ############################################################################
    # VARIABLES DE LA CLASSE

    _delta_temps: float = 0.0
    _delta_temps_fixe: float = 0.0

    _clock: pygame.time.Clock = pygame.time.Clock()

    ############################################################################
    # ASSESSEURS

    @property
    @classmethod
    def delta_temps(cls) -> float:
        return cls._delta_temps
    
    @property
    @classmethod
    def delta_temps_fixe(cls) -> float:
        return cls._delta_temps_fixe

    @property
    @classmethod
    def temps(cls) -> float:
        return pygame.time.get_ticks() * 1e-3
    
    ############################################################################
    # MÉTHODES D'ACTUALISATION DU TEMPS

    @classmethod
    def actualiser(cls) -> None:
        cls._delta_temps = cls._clock.tick()