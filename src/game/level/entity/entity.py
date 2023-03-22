import pygame

from abc import ABC, abstractmethod

from ..camera import Camera


class Entity(ABC):
    """
    Classe abstraite pour une entité. Toutes les entités doivent hériter de
    cette classe et implémenter les méthode abstraites.
    """

    def __init__(self, position: pygame.Vector2) -> None:
        """
        Constructeur.
        :param position: La position de l'entité.
        """
        super().__init__()
        self.position: pygame.Vector2 = position

    @abstractmethod
    def update(self) -> None:
        """
        Méthode appelée à chaque frame. La gestion des entrées doit se faire
        ici. (Doit être implémentée par la classe enfant)
        """

    @abstractmethod
    def fixed_update(self) -> None:
        """
        Méthode appelée à intervale régulier et un nombre de fois fixe par
        seconde. Les mouvements et la gestion de collision doit se faire ici.
        (Doit être implémentée dans une classe enfant)
        """

    @abstractmethod
    def draw(self, camera: Camera) -> None:
        """
        Dessiner l'entité à l'écran. (Doit être implémentée par la classe
        enfant)
        :param camera: La camera qui fait le rendu.
        """