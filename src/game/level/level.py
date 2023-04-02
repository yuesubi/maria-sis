import os
import sys
import pygame

from ...constants import EPSILON, UNIT
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
        prev_position = self.player.rect_collider.position
        self.player.fixed_update()

        self.detect_player_collision(prev_position)

        self.camera.position = self.camera.position.lerp(
            self.player.position + CAMERA_OFFSET,
            Time.fixed_delta_time * 4
        )

        self.camera.position.x = min(max(
            self.camera.position.x,
            self.level_map.top_left.x),
            self.level_map.bottom_right.x
        )
        self.camera.position.y = min(max(
            self.camera.position.y,
            self.level_map.top_left.y),
            self.level_map.bottom_right.y
        )
    
    def detect_player_collision(self, prev_position: pygame.Vector2) -> None:
        """
        Detection des collisions du joueur.
        :param prev_position: La position du joueur avant le mouvement.
        """

        # Trouver les blocks à vérifier (il y a besoin de vérifier que les
        # blocks autour du joueur)
        blocks_to_check = filter(
            # Seulement les blocks non None
            lambda block: block is not None,
            [
                # Récupérer le block
                self.level_map.block_at(
                    # Calculer la position du block
                    pygame.Vector2(position) + prev_position
                )
                for position in [
                    # Position relative des blocks par rapport au joueur
                    (1, -1), (1, 1), (-1, 1), (-1, -1),
                    (0, -1), (1, 0), (0, 1), (1, 0),
                    (0, 0)
                ]
            ]
        )

        # Part du mouvement effectué à conserver pour chaque axe
        x_t = 1.0
        y_t = 1.0

        # Pour chaque block à vérifier
        for block in blocks_to_check:
            # Si il y a collision
            if block.rect_collider.is_colliding_rect(self.player.rect_collider):
                # Calculer la part qu'on peut conserver pour que la collision
                # soit résolue
                new_x_t = min(
                    x_t,
                    block.rect_collider.resolve_collision_x_rewind(
                        self.player.rect_collider, prev_position
                    )
                )
                new_y_t = min(
                    y_t,
                    block.rect_collider.resolve_collision_y_rewind(
                        self.player.rect_collider, prev_position
                    )
                )

                # Choisir la plus grande part
                if new_x_t > new_y_t:
                    x_t = min(new_x_t, x_t)
                else:
                    y_t = min(new_y_t, y_t)
        
        delta_position = self.player.rect_collider.position - prev_position
        resolve_vector = pygame.Vector2(
            delta_position.x * x_t,
            delta_position.y * y_t
        )

        self.player.position -= delta_position
        self.player.position += resolve_vector

        # Remettre à zéro la vélocité si besoin.
        if x_t + EPSILON < 1.0:
            self.player.velocity.x = 0.0
        if y_t + EPSILON < 1.0:
            self.player.velocity.y = 0.0

    def update(self) -> None:
        self.player.update()
    
    def render_to(self, target_surf: pygame.Surface) -> None:
        self.camera.begin_render(target_surf)
        for block in self.level_map.near_blocks(self.camera.position):
            block.draw(self.camera)
        self.player.draw(self.camera)
        self.camera.end_render()