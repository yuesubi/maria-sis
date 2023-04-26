import pyray as pr
from itertools import chain
from typing import Iterator

from ....constants import CHUNK_WIDTH, CHUNK_HEIGHT, UNIT
from ....utils import Vec2
from ..block import Block, DecorativeBlock
from .chunk import Chunk


def color_hash(color: pr.Color) -> int:
    return color.r * (255 ** 3) + color.g * (255 ** 2) + color.b * (255) +  \
        color.a


BLOCK_OF_COLOR: dict[pr.Color, type[Block]] = {
    color_hash(pr.Color(0, 0, 0, 255)): DecorativeBlock
}


class LevelMap:
    """Classe qui représente la carte d'un niveau."""

    @classmethod
    def create_from_file(cls, img_path: str) -> 'LevelMap':
        """
        Crée une carte du niveau à partir d'une image, ou les couleurs de pixels
        sont associés à un type de block.
        :img_path: Le chemin de l'image.
        :return: La carte du niveau
        """
        level_map = cls()

        map_img = pr.load_image(img_path)
        level_map.top_left.xy = 0, 0
        level_map.bottom_right = Vec2(map_img.width, map_img.height) * UNIT

        for y in range(map_img.height):
            for x in range(map_img.width):
                chunk_pos = f"{x // CHUNK_WIDTH}x{y // CHUNK_HEIGHT}"

                # Crée un chunk si il y en a pas
                chunk = level_map._chunks.get(chunk_pos)
                if chunk is None:
                    chunk = Chunk()
                    level_map._chunks[chunk_pos] = chunk
                
                # Ajout du block
                color = pr.get_image_color()
                block_type = BLOCK_OF_COLOR.get(color_hash(color))
                if block_type is not None:
                    block = block_type(Vec2(x,y))
                    chunk[x % CHUNK_WIDTH, y % CHUNK_HEIGHT] = block
                elif color == pr.Color(0, 255, 0, 0):
                    level_map.spawn_point = Vec2(x, y)

        return level_map

    def __init__(self) -> None:
        """Constructeur."""

        self._chunks: dict[str, Chunk] = dict()
        self.spawn_point: Vec2 = Vec2.null

        self.top_left: Vec2 = Vec2.null
        self.bottom_right: Vec2 = Vec2.null
    
    def block_at(self, position: Vec2) -> Block | None:
        """
        Récupérer le block à la position donnée.
        :param position: La position du block à récupérer.
        :return: Le block si il est trouvé ou None sinon.
        """

        # Trouver la position du chunk et le récupérer.
        chunk_pos = (
            int(position.x) // CHUNK_WIDTH,
            int(position.y) // CHUNK_HEIGHT
        )
        chunk = self._chunks.get(f"{chunk_pos[0]}x{chunk_pos[1]}")

        block = None
        
        # Si le chunk existe récupérer le block
        if chunk is not None:
            block = chunk[
                int(position.x) - chunk_pos[0] * CHUNK_WIDTH,
                int(position.y) - chunk_pos[1] * CHUNK_HEIGHT
            ]
        
        return block
    
    def near_blocks(self, position: Vec2) -> Iterator[Block]:
        """
        Récupérer les blocks qui proches de la position donnée.
        :param position: La position à utiliser.
        :return: Un itérateur de tous les blocks.
        """
        return chain.from_iterable([
            chunk.blocks for chunk in self._near_chunks(position)
        ])

    def _near_chunks(self, position: Vec2) -> list[Chunk]:
        """
        Récupérer les chunks qui sont à coté de la position donnée.
        :param position: La position à utiliser.
        :return: Les chunks trouvés.
        """
        chunks = list()
        chunk_pos = (
            int(position.x) // CHUNK_WIDTH,
            int(position.y) // CHUNK_HEIGHT
        )

        for y in range(3):
            for x in range(3):
                pos = f"{chunk_pos[0] - 1 + x}x{chunk_pos[1] - 1 + y}"
                chunk = self._chunks.get(pos)
                if chunk is not None:
                    chunks.append(chunk)
        
        return chunks