import pygame

from ...assets import OVER_WORLD_TILES
from ...managers import Input, Time
from ..camera import Camera
from .block import Block


# XXX: Voici un example pour un bloc décoratif, pour que tu puisse voir comment
# hériter de DecorativeBlock et utiliser Camera


class DecorativeBlock(Block):
    """Classe d'un exemple de bloc décoratif."""

    def __init__(self, position: pygame.Vector2) -> None:
        """
        Constructeur.
        :param position: La position du bloc.
        """
        super().__init__(
            position
        )

        # TODO: Prendre en argument l'image du bloc et la stocker pour pouvoir
        # la dessiner

        # Remplir le masque de collision
        self.collision_mask.fill()
    
    def draw(self, camera: Camera) -> None:

        # Dessiner l'image du bloc
        camera.draw_surface(
            self.position,
            OVER_WORLD_TILES[0]
        )