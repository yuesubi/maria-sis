import pygame


class Time:
    """Classe statique qui gère les temps et les durées du jeu."""

    ############################################################################
    # VARIABLES DE LA CLASSE

    _fixed_delta_time: float = 0.0

    _clock: pygame.time.Clock = pygame.time.Clock()

    ############################################################################
    # ASSESSEURS

    @property
    @classmethod
    def delta_time(cls) -> float:
        """
        Assesseur du temps écoulé entre les deux actualisations.
        :return: Le temps écoulé entre les deux actualisations.
        """
        return cls._clock.get_time()
    
    @property
    @classmethod
    def fixed_delta_time(cls) -> float:
        """
        Assesseur du temps entre deux actualisations du mouvement.
        :return: Le temps entre deux actualisations du mouvement
        """
        return cls._fixed_delta_time

    @property
    @classmethod
    def current_time(cls) -> float:
        """
        Assesseur du temps.
        :return: Le temps.
        """
        return pygame.time.get_ticks() * 1e-3
    
    ############################################################################
    # MÉTHODES D'ACTUALISATION DU TEMPS

    @classmethod
    def update(cls) -> None:
        """Actualiser les variables de temps."""
        cls._clock.tick()