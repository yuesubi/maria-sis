from functools import filter
from typing import Iterator

from ....constants import *
from ..block import Block
from ..entity import Entity


class Chunk:
    """Un chunk du niveau."""

    def __init__(self) -> None:
        """Constructeur."""

        # Tous les blocks du chunk
        self._blocks: list[Block | None] = [
            None for _ in range(CHUNK_WIDTH * CHUNK_HEIGHT)
        ]

        self.entities: list[Entity] = list()
    
    def __setitem__(self, x_y: tuple[int, int], block: Block | None) -> None:
        """
        Change the content of a cell from the chunk.
        :param x_y: The position of the cell.
        :param block: The new content of the cell.
        """
        assert x_y[0] < CHUNK_WIDTH and not (x_y[0] < 0)
        assert x_y[1] < CHUNK_HEIGHT and not (x_y[1] < 0)
        self._blocks[x_y[0] + x_y[1] * CHUNK_WIDTH] = block

    def __getitem__(self, x_y: tuple[int, int]) -> Block:
        """
        Get the content of a cell from the chunk.
        :param x_y: The position of the cell.
        :return: The content of the cell.
        """
        assert x_y[0] < CHUNK_WIDTH and not (x_y[0] < 0)
        assert x_y[1] < CHUNK_HEIGHT and not (x_y[1] < 0)
        return self._blocks[x_y[0] + x_y[1] * CHUNK_WIDTH]

    @property
    def blocks(self) -> Iterator[Block]:
        """
        Récupérer tous les blocks.
        :return: Les blocks et leurs coordonnées.
        """
        return filter(lambda block: block is not None, self._blocks)