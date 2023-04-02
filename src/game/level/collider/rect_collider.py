import sys
import pygame

from ....constants import EPSILON


class RectCollider:
    """Détecteur de collision rectangulaire."""

    def __init__(self, position: pygame.Vector2, size: pygame.Vector2) -> None:
        """
        Constructeur.
        :param position: La position du centre du rectangle.
        :param size: La taille du rectangle.
        """
        # Le centre du rectangle
        self.position: pygame.Vector2 = position
        self.size: pygame.Vector2 = size

    @property
    def x(self) -> float:
        return self.position.x
    
    @x.setter
    def x(self, new_x: float) -> None:
        self.position.x = new_x

    @property
    def y(self) -> float:
        return self.position.y
    
    @y.setter
    def y(self, new_y: float) -> None:
        self.position.y = new_y

    @property
    def width(self) -> float:
        return self.size.x
    
    @width.setter
    def width(self, new_width: float) -> None:
        self.size.x = new_width
    
    @property
    def height(self) -> float:
        return self.size.y
    
    @height.setter
    def height(self, new_height: float) -> None:
        self.size.y = new_height
    
    def is_colliding_rect(self, other: 'RectCollider') -> bool:
        """
        Méthode qui permet de savoir si le rectangle est en collision avec un
        autre.
        :param other: L'autre rectangle avec lequel faire la vérification.
        :return: Vrai si les deux rectangles sont en collision, False sinon.
        """
        return abs(self.x - other.x) < (self.width + other.width) / 2 and \
            abs(self.y - other.y) < (self.height + other.height) / 2
    
    def resolve_collision_vector(self, other: 'RectCollider',
            other_previous_pos: pygame.Vector2) -> pygame.Vector2:
        
        # Calculer la distance entre les deux objets qu'il faut avoir pour qu'il
        # n'y ai pas de collision
        double_size = (self.size + other.size) / 2
        
        # Rectangle de collision de other après le déplacement Y
        moving = RectCollider(
            pygame.Vector2(other_previous_pos.x, other.y),
            other.size
        )

        # Si il y a collision
        if self.is_colliding_rect(moving):
            # Corriger la position Y pour qu'il n'y ai plus de collision
            y_distance = double_size.y - abs(moving.y - self.y) + EPSILON
            moving.y += y_distance * (1 if moving.y - self.y > 0 else -1)
        
        # Rectangle de collision de other après le déplacement X
        moving.x = other.position.x

        if self.is_colliding_rect(moving):
            # Corriger la position X pour qu'il n'y ai plus de collision
            x_distance = double_size.x - abs(moving.x - self.x) + EPSILON
            moving.x += x_distance * (1 if moving.x - self.x > 0 else -1)

        # Retourner le vecteur pour résoudre la collision
        return moving.position - other.position

    def resolve_collision_by_moving_other(self, other: 'RectCollider') -> None:
        """
        Résout la collision en déplaçant l'autre rectangle.
        :param other_rect: L'autre rectangle.
        """
        double_size = (self.size + other.size) / 2

        # Calculer la distance nécessaire pour sortir pour chaque axe
        x_distance = double_size.x - abs(other.x - self.x)
        y_distance = double_size.y - abs(other.y - self.y)

        if y_distance < x_distance:
            if other.y - self.y > 0:
                other.y += y_distance
            else:
                other.y -= y_distance
        else:
            if other.x - self.x > 0:
                other.x += x_distance
            else:
                other.x -= x_distance