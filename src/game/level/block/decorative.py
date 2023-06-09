import pyray as pr

from ....utils import Vec2
from ...assets import OVER_WORLD_TILES, OVER_WORLD_TILE_SET
from ..camera import Camera
from ..collider import RectCollider
from .block import Block


# XXX: Voici un example pour un bloc décoratif, pour que tu puisse voir comment
# hériter de DecorativeBlock et utiliser Camera


class DecorativeBlock(Block):
    """Classe d'un exemple de bloc décoratif."""

    def __init__(self, position: Vec2, block_id: int) -> None:
        """
        Constructeur.
        :param position: La position du bloc.
        :param block_id: L'id du block.
        """
        super().__init__(
            position
        )

        self.texture: pr.Texture = pr.load_texture(OVER_WORLD_TILE_SET)
        self.block_id = block_id
    
    @property
    def rect_collider(self) -> RectCollider:
        return RectCollider(self.position.copy, Vec2(1, 1))
    
    def draw(self, camera: Camera) -> None:
        # Dessiner l'image du bloc
        camera.draw_texture_part(
            self.texture,
            self.position,
            OVER_WORLD_TILES[self.block_id]
        )