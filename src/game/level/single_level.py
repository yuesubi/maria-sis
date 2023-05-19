import os
import pyray as pr

from ...constants import *
from ..managers import Time, Scene
from .camera import Camera
from .entity import Player
from .level import Level


class SingleLevelScene(Scene):
    """Le niveau en solo."""

    def __init__(self) -> None:
        """Constructeur."""
        super().__init__()

        map_path = os.path.join(os.path.dirname(__file__),
            "..", "..", "..", "maps", "sample.png")
        self.player = Player()

        self.level: Level = Level(set([self.player]), map_path)
        
        self.camera: Camera = Camera()
        self.camera.position = self.level.level_map.spawn_point.copy
    
    def fixed_update(self) -> None:
        if self.level.winner is None:
            self.level.fixed_update()
        
        self.camera.position = self.camera.position.lerp(
            self.player.position + CAMERA_OFFSET,
            Time.fixed_delta_time * 4
        )

        self.camera.position.x = min(max(
            self.camera.position.x,
            self.level.level_map.top_left.x + WIDTH_IN_BLOCKS/2 - 0.5),
            self.level.level_map.bottom_right.x - WIDTH_IN_BLOCKS/2 - 0.5
        )
        self.camera.position.y = min(max(
            self.camera.position.y,
            self.level.level_map.top_left.y + HEIGHT_IN_BLOCKS/2 - 0.5),
            self.level.level_map.bottom_right.y - HEIGHT_IN_BLOCKS/2 - 0.5
        )
    
    def update(self) -> None:
        inputs = Player.Inputs()
        inputs.pressing_left = pr.is_key_down(pr.KeyboardKey.KEY_LEFT)
        inputs.pressing_right = pr.is_key_down(pr.KeyboardKey.KEY_RIGHT)
        inputs.pressing_jump = pr.is_key_down(pr.KeyboardKey.KEY_SPACE)

        self.player.update(inputs)
    
    def render(self) -> None:
        self.camera.begin_render()
        
        for block in self.level.level_map.near_blocks(self.camera.position):
            block.draw(self.camera)
            
        for entity in self.level.entities:
            entity.draw(self.camera)
            
        self.camera.end_render()