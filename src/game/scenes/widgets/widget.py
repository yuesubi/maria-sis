import pygame
from typing import Union

from ....utils import Vec2
from .anchor import Anchor
from .fit import Fit


class Widget:
    """
    Classe représentant un élément de l'IHM. Tout les éléments de l'IHM doivent
    hériter de cette classe.
    """

    def __init__(
            self,
            position: Vec2,
            anchor: Anchor,
            size: Vec2,
            fit: Fit = Fit.NONE
        ) -> None:
        """
        Constructeur d'un élément de l'IHM.
        :param position: La position de l'élément.
        :param anchor: L'origine de la position.
        :param size: La taille de l'élément.
        :param fit: L'adaptation au parent. (optionnel)
        """
        
        self._parent: Widget | None = None
        self._anchor: Anchor = Anchor(anchor)
        self._fit: Fit = Fit(fit)

        self._position: Vec2 = position.copy
        self._size: Vec2 = size.copy
    
    ############################################################################
    # Méthodes qui peuvent être surchargées par les héritiers

    def update(self) -> None:
        """
        Mettre à jour l'élément. Chaque héritier de cette classe peut surcharger
        la méthode si besoin.
        """
    
    def render(self, target: pygame.Surface) -> None:
        """
        Faire le rendu de l'élément. Chaque héritier de cette classe peut
        surcharger la méthode si besoin.
        :param target: La surface sur laquelle faire le rendu.
        """
    
    ############################################################################
    # Assesseurs et modificateurs qui peuvent être surchargées par les héritiers
    
    @property
    def parent(self) -> Union['Widget', None]:
        return self._parent
    
    @parent.setter
    def parent(self, new_parent: Union['Widget', None]) -> None:
        self._parent = new_parent
    
    @property
    def anchor(self) -> Anchor:
        return self._anchor
    
    @anchor.setter
    def anchor(self, new_anchor: Anchor) -> None:
        self._anchor = new_anchor
    
    @property
    def fit(self) -> Fit:
        return self._fit
    
    @fit.setter
    def fit(self, new_fit: Fit) -> None:
        self._fit = new_fit
    
    @property
    def position(self) -> Vec2:
        return self._position
    
    @position.setter
    def position(self, new_position: Vec2) -> None:
        self._position = new_position
    
    @property
    def size(self) -> Vec2:
        return self._size
    
    @size.setter
    def size(self, new_size: Vec2) -> None:
        self._size = new_size
    
    ############################################################################
    # Méthodes classiques
    
    def global_position(self, part: Anchor) -> Vec2:
        """
        Retourne la position globale de l'élément. (Méthode recursive)
        :param part: La partie de l'élément dont on veut la position.
        :return: La position calculée.
        """
        global_position = self.position + self.position_of(part)

        # Si l'élément à un parent ajouter sa position globale
        if self.parent is not None:
            global_position += self.parent.global_position(self.anchor)
        
        return global_position

    def position_of(self, part: Anchor) -> Vec2:
        """
        Calcule la position locale d'une partie de l'élément.
        :param part: La partie de laquelle il faut calculer la position.
        :return: La position calculée.
        """
        return self.to_center() + self.center_to(part)

    def to_center(self) -> Vec2:
        """
        Trouver le vecteur de l'ancre au centre.
        :return: Le vecteur de l'ancre au centre.
        """
        return -self.center_to(self.anchor)

    def center_to(self, part: Anchor) -> Vec2:
        """
        Trouver le vecteur du centre à l'ancre.
        :return: Le vecteur du centre à l'ancre.
        """
        position = Vec2(0, 0)

        if part == Anchor.N:
            position = Vec2(0.0, self.size.y / -2.0)
        elif part == Anchor.E:
            position = Vec2(self.size.x / 2.0, 0.0)
        elif part == Anchor.S:
            position = Vec2(0.0, self.size.y / 2.0)
        elif part == Anchor.W:
            position = Vec2(self.size.x / -2.0, 0.0)

        elif part == Anchor.NE:
            position = Vec2(self.size.x / 2.0, self.size.y / -2.0)
        elif part == Anchor.SE:
            position = self.size / 2.0
        elif part == Anchor.SW:
            position = Vec2(self.size.x / -2.0, self.size.y / 2.0)
        elif part == Anchor.NW:
            position = self.size / -2.0

        return position