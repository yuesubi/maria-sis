import pygame

from ....constants import UNIT
from ....utils import Vec2
from ...assets import OVER_WORLD_TILES
from ..camera import Camera
from ..collider import RectCollider
from .block import Block


# XXX: Voici un example pour un bloc décoratif, pour que tu puisse voir comment
# hériter de DecorativeBlock et utiliser Camera


class DecorativeBlock(Block):
    """Classe d'un exemple de bloc décoratif."""

    def __init__(self, position: Vec2) -> None:
        """
        Constructeur.
        :param position: La position du bloc.
        """
        super().__init__(
            position
        )

        # TODO: Prendre en argument l'image du bloc et la stocker pour pouvoir
        # la dessiner
    
    @property
    def rect_collider(self) -> RectCollider:
        return RectCollider(self.position.copy, Vec2(1, 1))
    
    def draw(self, camera: Camera) -> None:
        # Dessiner l'image du bloc
        camera.draw_surface(
            self.position,
            OVER_WORLD_TILES[0]
        )