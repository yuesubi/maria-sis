import pygame

from abc import ABC, abstractmethod, abstractproperty

from ....utils import Vec2
from ..camera import Camera
from ..collider import RectCollider


class Block(ABC):
    """
    Classe abstraite pour un bloc. Tous les blocs doivent hériter de cette
    classe et implémenter les méthode abstraites.
    """

    def __init__(self, position: Vec2) -> None:
        """
        Constructeur.
        :param position: La position du bloc.
        """
        super().__init__()

        # La position est un vecteur mais en gros c'est un point, il y a juste
        # pas de classe Point dans pygame.
        self.position: Vec2 = position
    
    @abstractproperty
    def rect_collider(self) -> RectCollider:
        """
        Assesseur du rectangle de collision.
        :return: Le rectangle de collision.
        """

    @abstractmethod
    def draw(self, camera: Camera) -> None:
        """
        Dessiner le bloc à l'écran. (Doit être implémentée par la classe
        enfant)
        :param camera: La camera qui fait le rendu.
        """