"""Vecteur mathématique à 2 dimensions."""

import math
from typing import Any

from ..custom_decorators import ClassGetter


class Vec2:
    """Vecteur mathématique à 2 dimensions."""

    ############################################################################
    # CONSTRUCTEURS

    @classmethod
    def from_xy(cls, xy: tuple[float, float]) -> 'Vec2':
        """
        Constructeur d'un Vec2 à partir des coordonnées.
        :param xy: Le tuple avec les coordonnées (x, y).
        :return: Le Vec2 des coordonnées données.
        """
        return Vec2(xy[0], xy[1])

    @classmethod
    def from_yx(cls, yx: tuple[float, float]) -> 'Vec2':
        """
        Constructeur d'un Vec2 à partir des coordonnées.
        :param yx: Le tuple avec les coordonnées (y, x).
        :return: Le Vec2 des coordonnées données.
        """
        return Vec2(yx[1], yx[0])

    @ClassGetter
    def null(cls) -> 'Vec2':
        """
        Constructeur d'un Vec2 de coordonnées (0, 0).
        :return: Un Vec2 de coordonnées (0, 0).
        """
        return Vec2(0.0, 0.0)
    
    def __init__(self, x: float, y: float) -> None:
        """
        Constructeur d'un Vec2 de coordonnées (x, y).
        :param x: La coordonnée x du Vec2.
        :param y: La coordonnée y du Vec2.
        :return: Un Vec2 de coordonnées (x, y).
        """
        self.x: float = x
        self.y: float = y
    
    ############################################################################
    # PROPRIÉTÉS
    
    @property
    def is_null(self) -> bool:
        """True si les coordonnées du Vec2 sont (0, 0), False sinon."""
        return self.x == 0.0 and self.y == 0.0
    
    @property
    def copy(self) -> 'Vec2':
        """Une copie du Vec2."""
        return Vec2(self.x, self.y)
    
    ############################################################################
    # FONCTIONNEMENT DE L'OBJET
    
    def __repr__(self) -> str:
        return f"Vec2<{self.x},{self.y}>"
    
    ############################################################################
    # COMPARAISONS

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vec2):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __ne__(self, other: object) -> bool:
        if not isinstance(other, Vec2):
            return NotImplemented
        return not self == other
    
    ############################################################################
    # OPÉRATIONS

    def len(self) -> float:
        """Calculer la norme du vecteur."""
        return math.sqrt(self.x*self.x + self.y*self.y)

    def sqrd_len(self) -> float:
        """Calculer la norme carrée du vecteur."""
        return self.x*self.x + self.y*self.y

    def dot(self, other: 'Vec2') -> float:
        """
        Produit scalaire du Vec2 avec other.
        :param other: L'autre Vec2 avec lequel faire le produit scalaire.
        :return: Le résultat du produit scalaire.
        """
        return self.x * other.x + self.y * other.y
    
    def lerp(self, target: 'Vec2', amount: float) -> 'Vec2':
        """
        Calculer une interpolation linéaire de ce Vec2 vers le Vec2 cible de
        amount.
        :param other: Le Vec2 cible.
        :param amount: La distance de l'interpolation. 0.0 donne ce Vec2 et 1.0
            donne le Vec2 cible.
        :return: L'interpolation linéaire calculée.
        """
        return self + (target - self) * amount
    
    def rotate(self, theta: float) -> None:
        """
        Faire pivoter cd Vec2 de theta radians.
        :param theta: Le nombre de radians duquel il faut tourner.
        """
        # Calcul de rotation avec les nombres complexes
        # (x + i*y) * (cos(theta) + i*sin(theta)) =
        # x*cos(theta) - y*sin(theta) + i*(x*sin(theta) + y*cos(theta))
        x, y = self.x, self.y
        cos_theta, sin_theta = math.cos(theta), math.sin(theta)
        self.x, self.y = x*cos_theta - y*sin_theta, x*sin_theta + y*cos_theta
    
    def rotation(self, theta: float) -> 'Vec2':
        """
        Calculer la rotation de ce Vec2 de theta radians.
        :param theta: Le nombre de radians duquel il faut tourner.
        :return: La rotation de ce Vec2.
        """
        vec = self.copy
        vec.rotate(theta)
        return vec
    
    def __add__(self, other: 'Vec2') -> 'Vec2':
        """Somme de ce Vec2 et de other."""
        return Vec2(self.x + other.x, self.y + other.y)
    
    #def __radd__(self, other: 'Vec2') -> 'Vec2':
    #    """Somme de ce Vec2 et de other."""
    #    return self.__add__(other)
    
    def __iadd__(self, other: 'Vec2') -> 'Vec2':
        """Ajouter other à ce Vec2."""
        self.x += other.x
        self.y += other.y
        return self.copy

    def __sub__(self, other: 'Vec2') -> 'Vec2':
        """Différence entre ce Vec2 et other."""
        return Vec2(self.x - other.x, self.y - other.y)

    #def __rsub__(self, other: 'Vec2') -> 'Vec2':
    #    """Différence entre other et ce Vec2."""
    #    return Vec2(other.x - self.x, other.y - self.y)
    
    def __isub__(self, other: 'Vec2') -> 'Vec2':
        """Soustraire other à ce Vec2."""
        self.x -= other.x
        self.y -= other.y
        return self.copy
    
    def __mul__(self, scalar: float) -> 'Vec2':
        """Produit de ce Vec2 et de scalar."""
        return Vec2(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar: float) -> 'Vec2':
        """Produit de ce Vec2 et de scalar."""
        return self.__mul__(scalar)
    
    def __imul__(self, scalar: float) -> 'Vec2':
        """Multiplier ce Vec2 par scalar."""
        self.x *= scalar
        self.y *= scalar
        return self.copy
    
    def __div__(self, inv_scalar: float) -> 'Vec2':
        """Rapport entre ce Vec2 et inv_scalar."""
        return Vec2(self.x / inv_scalar, self.y / inv_scalar)
    
    def __truediv__(self, inv_scalar: float) -> 'Vec2':
        """Rapport entre ce Vec2 et inv_scalar."""
        return Vec2(self.x / inv_scalar, self.y / inv_scalar)
    
    def __idiv__(self, inv_scalar: float) -> 'Vec2':
        """Diviser ce Vec2 par inv_scalar."""
        self.x /= inv_scalar
        self.y /= inv_scalar
        return self.copy
    
    def __pos__(self) -> 'Vec2':
        """Une copie de ce Vec2."""
        return self.copy
    
    def __neg__(self) -> 'Vec2':
        """L'opposé de ce Vec2."""
        return Vec2(-self.x, -self.y)

    ############################################################################
    # Assesseur et modificateurs de tuples

    @property
    def xy(self) -> tuple[float, float]:
        """Le tuple (x, y)."""
        return self.x, self.y
    
    @xy.setter
    def xy(self, xy: tuple[float, float]) -> None:
        """Remplacer les cordonnées par xy."""
        self.x, self.y = xy

    @property
    def yx(self) -> tuple[float, float]:
        """Le tuple (y, x)."""
        return self.y, self.x
    
    @yx.setter
    def yx(self, yx: tuple[float, float]) -> None:
        """Remplacer les cordonnées par yx."""
        self.y, self.x = yx
    
    @property
    def xx(self) -> tuple[float, float]:
        """Le tuple (x, x)."""
        return self.x, self.x
    
    @property
    def yy(self) -> tuple[float, float]:
        """Le tuple (y, y)."""
        return self.y, self.y