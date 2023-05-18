import os

from ...constants import EPSILON
from ...utils import Vec2
from ..managers import Scene
from .entity import Entity, Player
from .level_map import LevelMap


class Level(Scene):
    """Un niveau."""
    
    def __init__(self, players: set[Player], map_path: str) -> None:
        """
        Constructeur.
        :param players: Les joueurs.
        :param map_path: Le chemin vers la carte du niveau.
        """
        super().__init__()

        self.level_map = LevelMap.create_from_file(map_path)
        spawn_point = self.level_map.spawn_point + Vec2(0, -0.5)

        self.players: set[Player] = players
        for player in self.players:
            player.position = spawn_point.copy

        self.entities: set[Entity] = set(self.players)
    
    def fixed_update(self) -> None:
        for entity in self.entities:
            prev_pos = entity.position.copy
            entity.fixed_update()

            resolve_vec = self._detect_block_collision(entity, prev_pos)
            if abs(resolve_vec.x) > EPSILON or abs(resolve_vec.y) > EPSILON:
                entity.on_collision(resolve_vec)

        for player in self.players:
            if player.position.y > 20:
                player.position.y = 0
    
    def _detect_block_collision(self, entity, prev_position: Vec2) -> Vec2:
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