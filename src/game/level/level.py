import os
import pygame

from ...constants import UNIT
from ..managers import Time, Scene
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
        for block in self.level_map.near_blocks(self.camera.position):
            block_size = pygame.Vector2(block.collision_mask.get_size()) / UNIT
            block_tl = block.position - block_size / 2

            player_size = pygame.Vector2(self.player.collision_mask.get_size())
            player_size /= UNIT
            player_tl = self.player.position - player_size / 2

            is_colliding = self.player.collision_mask.overlap(
                block.collision_mask,
                (block_tl - player_tl) * UNIT
            )

            if is_colliding:
                self.resolve_player_collision(prev_position)
    
    def resolve_player_collision(self, prev_position: pygame.Vector2) -> None:
        # print((self.player.position - block.position).x)
        pass

    def update(self) -> None:
        self.player.update()
    
    def render_to(self, target_surf: pygame.Surface) -> None:
        self.camera.begin_render(target_surf)
        for block in self.level_map.near_blocks(self.camera.position):
            block.draw(self.camera)
        self.player.draw(self.camera)
        self.camera.end_render()