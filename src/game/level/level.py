import os
import pygame

from ..managers import Time, Scene
from .camera import Camera
from .entity import Player
from .level_map import LevelMap


CAMERA_OFFSET: pygame.Vector2 = pygame.Vector2(0, -3)


class LevelScene(Scene):
    """Scène de niveau."""
    
    def __init__(self) -> None:
        super().__init__()

        map_path = os.path.join(os.path.dirname(__file__), "..", "..", "..",
            "maps", "sample.png")
        self.level_map = LevelMap.create_from_file(map_path)

        self.player: Player = Player()
        self.player.position = self.level_map.spawn_point
        self.camera: Camera = Camera()
        self.camera.position = self.player.position
    
    def fixed_update(self) -> None:
        self.player.fixed_update()
        self.camera.position = self.camera.position.lerp(
            self.player.position + CAMERA_OFFSET,
            Time.fixed_delta_time * 4
        )

    def update(self) -> None:
        self.player.update()
    
    def render_to(self, target_surf: pygame.Surface) -> None:
        self.camera.begin_render(target_surf)
        for block in self.level_map.near_blocks(self.camera.position):
            block.draw(self.camera)
        self.player.draw(self.camera)
        self.camera.end_render()