import os, time

from ...constants import EPSILON
from ...utils import Vec2
from ..managers import Time, Scene
from .camera import Camera
from .entity import Entity, Player
from .level_map import LevelMap


CAMERA_OFFSET: Vec2 = Vec2(0, -2)


class LevelScene(Scene):
    """Scène de niveau."""
    
    def __init__(self) -> None:
        super().__init__()

        map_path = os.path.join(os.path.dirname(__file__), "..", "..", "..",
            "maps", "sample.png")
        self.level_map = LevelMap.create_from_file(map_path)

        self.player: Player = Player()
        self.player.position = self.level_map.spawn_point + Vec2(0, -0.5)

        self.entities: set[Entity] = set()
        self.entities.add(self.player)
        
        self.camera: Camera = Camera()
        self.camera.position = self.player.position.copy
    
    def fixed_update(self) -> None:
        for entity in self.entities:
            prev_pos = entity.position.copy
            entity.fixed_update()

            resolve_vec = self.detect_block_collision(entity, prev_pos)
            if abs(resolve_vec.x) > EPSILON or abs(resolve_vec.y) > EPSILON:
                entity.on_collision(resolve_vec)

        if self.player.position.y > 20:
            self.player.position.y = 0
        
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
    
    def detect_block_collision(self, entity, prev_position: Vec2) -> Vec2:
        """
        Detection des collisions d'une entité avec les blocks.
        :param entity: L'entité.
        :param prev_position: La position avant le mouvement.
        :return: La translation qui résout l'éventuelle collision.
        """

        # Trouver les blocks à vérifier (il y a besoin de vérifier que les
        # blocks autour du joueur)
        blocks_to_check = (
            block for block in (
                # Récupérer le block
                self.level_map.block_at(
                    # Calculer la position du block
                    Vec2.from_xy(position) + prev_position
                )
                for position in [
                    # Position relative des blocks par rapport au joueur
                    (1, -1), (1, 1), (-1, 1), (-1, -1),
                    (0, -1), (1, 0), (0, 1), (1, 0),
                    (0, 0)
                ]
            )
            # Seulement les blocks non None
            if block is not None
        )

        # Part du mouvement effectué à conserver pour chaque axe
        x_t = 1.0
        y_t = 1.0

        # Pour chaque block à vérifier
        for block in blocks_to_check:
            # Si il y a collision
            if block.rect_collider.is_colliding_rect(entity.rect_collider):
                # Calculer la part qu'on peut conserver pour que la collision
                # soit résolue
                new_x_t = min(
                    x_t,
                    block.rect_collider.resolve_collision_x_rewind(
                        entity.rect_collider, prev_position
                    )
                )
                new_y_t = min(
                    y_t,
                    block.rect_collider.resolve_collision_y_rewind(
                        entity.rect_collider, prev_position
                    )
                )

                # Choisir la plus grande part
                if new_x_t > new_y_t:
                    x_t = new_x_t
                else:
                    y_t = new_y_t
        
        delta_position = entity.position - prev_position
        resolve_vector = Vec2(
            delta_position.x * x_t,
            delta_position.y * y_t
        )

        return resolve_vector - delta_position

    def update(self) -> None:
        self.player.update()

        for entity in self.entities:
            entity.update()
    
    def render(self) -> None:
        self.camera.begin_render()
        
        for block in self.level_map.near_blocks(self.camera.position):
            block.draw(self.camera)
            
        self.player.draw(self.camera)
        
        for entity in self.entities:
            entity.draw(self.camera)
            
        self.camera.end_render()