from abc import ABC, abstractmethod

from ..camera import Camera


class Block(ABC):
    """
    Classe abstraite pour un block. Tous les blocks doivent hériter de cette
    classe et implémenter les méthode abstraites.
    """

    @abstractmethod
    def draw(self, camera: Camera) -> None:
        """
        Dessiner le block à l'écran. (Doit être implémentée par la classe
        enfant)
        :param camera: La camera qui fait le rendu.
        """