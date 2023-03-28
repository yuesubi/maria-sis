import pygame

from abc import ABC, abstractmethod

from ....constants import UNIT
from ..camera import Camera


class Block(ABC):
    """
    Classe abstraite pour un bloc. Tous les blocs doivent hériter de cette
    classe et implémenter les méthode abstraites.
    """

    def __init__(self, position: pygame.Vector2) -> None:
        """
        Constructeur.
        :param position: La position du bloc.
        """
        super().__init__()

        # La position est un vecteur mais en gros c'est un point, il y a juste
        # pas de classe Point dans pygame.
        self.position: pygame.Vector2 = position

        # Masque pour les collisions
        self._collision_mask: pygame.mask.Mask = pygame.mask.Mask((UNIT, UNIT))
    
    @property
    def collision_mask(self) -> pygame.mask.Mask:
        """
        Assesseur du masque de collisions.
        :return: Le masque de collisions.
        """
        return self._collision_mask

    @abstractmethod
    def draw(self, camera: Camera) -> None:
        """
        Dessiner le bloc à l'écran. (Doit être implémentée par la classe
        enfant)
        :param camera: La camera qui fait le rendu.
        """