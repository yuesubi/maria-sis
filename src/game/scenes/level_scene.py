import abc
import os
import pyray as pr

from ...constants import *
from ..managers import Time, Scene
from ..level import Camera, Player, Level


class LevelScene(Scene):
    """La classe dont toutes les autres scènes de niveau doivent dériver."""

    def __init__(self, players: set[Player], main_player: Player) -> None:
        """
        Constructeur.
        :param players: Tous les joueurs.
        :param main_player: Le joueur qu'il faut suivre. (Doit faire partie de
            players)
        """
        super().__init__()

        map_path = os.path.join(os.path.dirname(__file__),
            "..", "..", "..", "maps", "sample.png")
        self.main_player = main_player

        self.level: Level = Level(players, map_path)
        
        self.camera: Camera = Camera()
        self.camera.position = self.level.level_map.spawn_point.copy

        self.pause_menu: int = 0
    
    def fixed_update(self, should_update_level=True) -> None:
        if self.level.winner is None and should_update_level:
            self.level.fixed_update()
        
        self.camera.position = self.camera.position.lerp(
            self.main_player.position + CAMERA_OFFSET,
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
    
    def render(self) -> None:
        self.camera.begin_render()
        
        for block in self.level.level_map.near_blocks(self.camera.position):
            block.draw(self.camera)
            
        for entity in self.level.entities:
            entity.draw(self.camera)
            
        self.camera.end_render()