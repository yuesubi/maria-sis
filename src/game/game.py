"""Jeu Maria Sis"""

import pyray as pr

from typing import Any, cast

from ..constants import SCALE, UNIT
from .level import LevelScene
from .managers import CreateSceneCallBack, Scene, SceneId, Time
from .menus import *


WIDTH, HEIGHT = 16, 13


SCENE_MAP: dict[SceneId, type[Scene]] = {
    SceneId.CONNECT_METHOD_MENU: ConnectMethodMenuScene,
    SceneId.HOST_OR_CLIENT_MENU: HostOrClientMenuScene,
    SceneId.HUB_CLIENT_MENU: HubClientMenuScene,
    SceneId.HUB_HOST_MENU: HubHostMenuScene,
    SceneId.LEVEL: LevelScene,
    SceneId.MAIN_MENU: MainMenuScene,
    SceneId.SCAN_MENU: ScanMenuScene,
}


class Game:
    """Jeu Maria Sis"""

    def __init__(self) -> None:
        """Constructeur."""
        pr.init_window(
            int(WIDTH * UNIT * SCALE), int(HEIGHT * UNIT * SCALE),
            "Maria Sis"
        )
        pr.set_trace_log_level(pr.TraceLogLevel.LOG_ERROR)
    
        Scene.set_create_scene_callback(
            cast(CreateSceneCallBack, self.create_scene)
        )
        Scene.push_scene(SceneId.MAIN_MENU)
        
        Time.set_fixed_fps(100)
    
    def create_scene(self, scene_id: SceneId, *scene_args: Any,
            **scene_kwargs: Any) -> Scene:
        """
        Méthode appelée pour créer une scène.
        :param new_scene_id: L'identifiant de la scène à créer.
        :param *scene_args: Les argument à donner au constructeur de la scène.
        :param *scene_kwargs: Les argument clés à donner au constructeur de la
            scène.
        """
        return SCENE_MAP[SceneId(scene_id)](*scene_args, **scene_kwargs)

    def run(self) -> None:
        """Faire tourner le jeu."""

        pr.set_target_fps(Time.fixed_fps*2)
        time_bank: float = 0.0
        
        while not pr.window_should_close():
            Scene.current_scene.update()
            
            time_bank = min(0.2, time_bank + Time.delta_time)
            while time_bank > Time.fixed_delta_time:
                Scene.current_scene.fixed_update()
                time_bank -= Time.fixed_delta_time
            
            pr.begin_drawing()
            pr.clear_background(pr.Color(150, 150, 150))

            Scene.current_scene.render()
            # pr.draw_fps(8, 8)
            # pr.draw_text(str(round(Time.fixed_fps)) + " fixed fps", 8, 28, 20, pr.WHITE)
            
            pr.end_drawing()
            
            Time.update()
        
        # Fermer les scènes
        while len(Scene._scene_stack) > 0:
            Scene.pop_scene()