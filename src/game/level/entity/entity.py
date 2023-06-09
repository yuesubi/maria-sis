from abc import ABC, abstractmethod

from ....utils import Vec2
from ..camera import Camera
from ..collider import RectCollider


class Entity(ABC):
    """
    Classe abstraite pour une entité. Toutes les entités doivent hériter de
    cette classe et implémenter les méthode abstraites.
    """

    def __init__(self, position: Vec2, size: Vec2) -> None:
        """
        Constructeur.
        :param position: La position.
        :param size: La taille.
        """
        super().__init__()
        self.position: Vec2 = position
        self.size: Vec2 = size
    
    @property
    def rect_collider(self) -> RectCollider:
        """
        Assesseur du rectangle de collision.
        :return: Le rectangle de collision.
        """
        return RectCollider(self.position.copy, self.size.copy)
    
    @abstractmethod
    def on_collision(self, resolve_vec: Vec2) -> None:
        """
        Méthode appelée quand une collision est résolue. Il faut au minimum
        appliquer le vecteur de résolution. (Doit être implémentée par la classe
        enfant)
        :param resolve_vec: La translation qui résout la collision.
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