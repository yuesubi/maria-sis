import os
import pyray as pr

from ...constants import *
from ..level import Player
from .level_scene import LevelScene


class SingleLevelScene(LevelScene):
    """Le niveau en solo."""

    def __init__(self) -> None:
        player = Player()
        super().__init__(
            players={ player },
            main_player=player
        )

    def update(self) -> None:
        super().update()

        inputs = Player.Inputs()
        inputs.pressing_left = pr.is_key_down(pr.KeyboardKey.KEY_LEFT)
        inputs.pressing_right = pr.is_key_down(pr.KeyboardKey.KEY_RIGHT)
        inputs.pressing_jump = pr.is_key_down(pr.KeyboardKey.KEY_SPACE)
        self.main_player.update(inputs)