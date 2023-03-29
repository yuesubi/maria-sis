import os
import math
import pygame

from ...constants import UNIT
from ..managers import Time, Scene
from .block import Block
from .camera import Camera
from .entity import Player
from .level_map import LevelMap


CAMERA_OFFSET: pygame.Vector2 = pygame.Vector2(0, -2)


class LevelScene(Scene):
    """Scène de niveau."""
    
    def __init__(self) -> None:
        super().__init__()

        map_path = os.path.join(os.path.dirname(__file__), "..", "..", "..",
            "maps", "sample.png")
        self.level_map = LevelMap.create_from_file(map_path)

        self.player: Player = Player()
        self.player.position = self.level_map.spawn_point + \
            pygame.Vector2(0, -0.5)
        self.camera: Camera = Camera()
        self.camera.position = self.player.position
    
    def fixed_update(self) -> None:
        prev_position = self.player.position
        self.player.fixed_update()

        self.detect_player_collision(prev_position)

        self.camera.position = self.camera.position.lerp(
            self.player.position + CAMERA_OFFSET,
            Time.fixed_delta_time * 4
        )
    
    def detect_player_collision(self, prev_position: pygame.Vector2) -> None:
        """
        Detection des collisions du joueur.
        :param prev_position: La position du joueur avant le mouvement.
        """
        player_rect = self.player.rect_collider
        
        for block in self.level_map.near_blocks(self.camera.position):
            if block.rect_collider.is_colliding_rect(player_rect):
                block.rect_collider.resolve_collision_by_moving_other(
                    player_rect
                )
        
        self.player.position = player_rect.position - pygame.Vector2(0, 0.5)

    def update(self) -> None:
        self.player.update()
    
    def render_to(self, target_surf: pygame.Surface) -> None:
        self.camera.begin_render(target_surf)
        for block in self.level_map.near_blocks(self.camera.position):
            block.draw(self.camera)
        self.player.draw(self.camera)
        self.camera.end_render()