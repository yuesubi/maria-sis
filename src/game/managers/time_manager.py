import time

from ...utils import ClassGetter


class Time:
    """Classe statique qui gère les temps et les durées du jeu."""

    ############################################################################
    # VARIABLES DE LA CLASSE

    _time: int = time.time_ns()

    _fps: float = 1.0
    _delta_time: float = 1.0

    _fixed_fps: float = 1.0
    _fixed_delta_time: float = 1.0

    ############################################################################
    # ASSESSEURS

    @ClassGetter
    def delta_time(cls) -> float:
        """
        Assesseur du temps écoulé entre les deux actualisations.
        :return: Le temps écoulé entre les deux actualisations.
        """
        return cls._delta_time
    
    @ClassGetter
    def fixed_delta_time(cls) -> float:
        """
        Assesseur du temps entre deux actualisations du mouvement.
        :return: Le temps entre deux actualisations du mouvement
        """
        return cls._fixed_delta_time

    @ClassGetter
    def time(cls) -> float:
        """
        Assesseur du temps.
        :return: Le temps.
        """
        return cls._time * 1E-9
    
    @ClassGetter
    def fps(cls) -> float:
        """
        Assesseur du nombre de fps.
        :return: Le nombre de fps.
        """
        return 1 / cls._delta_time if cls._delta_time != 0.0 else 0.0
    
    @ClassGetter
    def fixed_fps(cls) -> float:
        """
        Assesseur du nombre de fps fixe.
        :return: Le nombre de fps fixe.
        """
        return cls._fixed_fps
    
    ############################################################################
    # MÉTHODES STATIQUES CLASSIQUES

    @classmethod
    def set_fixed_fps(cls, fixed_fps: float) -> None:
        """
        Changer le nombre de actualisations fixes par seconde.
        :param fixed_fps: Le nouveau nombre de actualisations fixes par seconde.
        """
        cls._fixed_fps = fixed_fps
        cls._fixed_delta_time = 1 / fixed_fps if fixed_fps != 0 else 0.0
    
    @classmethod
    def set_fixed_delta_time(cls, fixed_delta_time: float) -> None:
        """
        Changer l'intervale de temps entre les actualisations fixes.
        :param fixed_delta_time: Le nouvel l'intervale de temps entre les
            actualisations fixes.
        """
        cls._fixed_delta_time = fixed_delta_time
        cls._fixed_fps = (1 / fixed_delta_time if fixed_delta_time != 0.0
            else 0.0)

    @classmethod
    def update(cls) -> None:
        """Actualiser les variables de temps."""

        _new_time = time.time_ns()
        cls._delta_time = (_new_time - cls._time) * 1E-9
        cls._time = _new_time