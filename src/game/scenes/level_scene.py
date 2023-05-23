import os
import pyray as pr

from ...constants import *
from ..managers import Time, Scene, SceneId
from ..level import Camera, Player, Level
from .widgets import *


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

        self._is_pause_menu_open: bool = False
        self._pause_menu: Frame = Frame(
            Vec2(0, 0), Anchor.NW,
            Vec2.null, Fit.NONE,
            children=[
                Frame(
                    Vec2(0, 0), Anchor.C,
                    Vec2(240, 240), Fit.NONE,
                    background_color=pr.Color(200, 100, 200, 255),
                    border_color=pr.Color(255, 100, 255, 255), border_width=3,
                    children=[
                        Text(
                            Vec2(0, -60), Anchor.C,
                            "Menu de Pause",
                            pr.Color(0, 0, 0, 255),
                            font_size=26
                        ),
                        TextButton(
                            Vec2(0, 0), Anchor.C,
                            Vec2(150, 50), Fit.NONE,
                            "Reprendre", pr.Color(0, 0, 0, 255), 20,
                            background_color=pr.Color(200, 100, 200, 255),
                            border_color=pr.Color(255, 100, 255, 255),
                            border_width=3,
                            command=self.close_pause_menu
                        ),
                        TextButton(
                            Vec2(0, 60), Anchor.C,
                            Vec2(150, 50), Fit.NONE,
                            "Quitter", pr.Color(0, 0, 0, 255), 20,
                            background_color=pr.Color(200, 100, 200, 255),
                            border_color=pr.Color(255, 100, 255, 255),
                            border_width=3,
                            command=lambda:
                                Scene.switch_scene(SceneId.MAIN_MENU)
                        )
                    ]
                )
            ]
        )
    
    def update(self) -> None:
        self._pause_menu.update()
    
    def fixed_update(self, should_update_level=True) -> None:
        if self.level.winner is None and should_update_level and \
                not self._is_pause_menu_open:
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

        if self._is_pause_menu_open:
            self._pause_menu.size.xy = pr.get_screen_width(), pr.get_screen_height()
            self._pause_menu.render()
    
    def open_pause_menu(self) -> None:
        """Ouvrir le menu de pause."""
        self._is_pause_menu_open = True
    
    def close_pause_menu(self) -> None:
        """Fermer le menu de pause."""
        self._is_pause_menu_open = False