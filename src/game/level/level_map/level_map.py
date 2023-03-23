import pygame

from itertools import chain
from typing import Iterator

from ....constants import CHUNK_WIDTH, CHUNK_HEIGHT
from ..block import Block
from .chunk import Chunk


class LevelMap:
    """Classe qui représente la carte d'un niveau."""

    @classmethod
    def create_from_file(cls, file_path: str) -> 'LevelMap':
        raise NotImplemented()

    def __init__(self) -> None:
        """Constructeur."""

        self._chunks: dict[str, Chunk] = dict()
    
    def near_blocks(self, position: pygame.Vector2) -> Iterator[Block]:
        """
        Récupérer les blocks qui proches de la position donnée.
        :param position: La position à utiliser.
        :return: Un itérateur de tous les blocks.
        """
        return chain.from_iterable([
            chunk.blocks for chunk in self._near_chunks(position)
        ])
    
    def _near_chunks(self, position: pygame.Vector2) -> list[Chunk]:
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