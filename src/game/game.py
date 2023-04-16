"""Jeu Maria Sis"""

import pygame

from typing import Any

from ..constants import SCALE, UNIT
from .level import LevelScene
from .managers import Input, Scene, SceneId, Time
from .scenes import MainMenuScene


WIDTH, HEIGHT = 16, 13


class Game:
    """Jeu Maria Sis"""

    def __init__(self) -> None:
        """Constructeur."""
        pygame.init()
        pygame.font.init()
        
        self.window = pygame.display.set_mode((
            WIDTH * UNIT * SCALE,
            HEIGHT * UNIT * SCALE
        ))
        pygame.display.set_caption("Maria Sis")
    
        Scene.set_create_scene_callback(self.create_scene)
        Scene.push_scene(SceneId.LEVEL)
        
        Time.set_fixed_fps(40)
    
    def create_scene(self, scene_id: SceneId, *scene_args: Any,
            **scene_kwargs: Any) -> Scene:
        """
        Méthode appelée pour créer une scène.
        :param new_scene_id: L'identifiant de la scène à créer.
        :param *scene_args: Les argument à donner au constructeur de la scène.
        :param *scene_kwargs: Les argument clés à donner au constructeur de la
            scène.
        """
        new_scene = None

        if scene_id == SceneId.LEVEL:
            new_scene = LevelScene(*scene_args, **scene_kwargs)
        elif scene_id == SceneId.MAIN_MENU:
            new_scene = MainMenuScene(*scene_args, **scene_kwargs)
        else:
            raise BaseException(f"scene id {scene_id} is not valid")
        
        return new_scene

    def run(self) -> None:
        """Faire tourner le jeu."""

        surf = pygame.Surface((WIDTH * UNIT, HEIGHT * UNIT))
        font = pygame.font.SysFont("", 16)
        
        time_bank: float = 0.0

        running = True
        
        while running:
            Input.update()
            if Input.is_quitting == True:
                running = False
            
            Scene.current_scene.update()
            
            time_bank = min(0.2, time_bank + Time.delta_time)
            while time_bank > Time.fixed_delta_time:
                Scene.current_scene.fixed_update()
                time_bank -= Time.fixed_delta_time
            
            surf.fill((150, 150, 150))
            Scene.current_scene.render_to(surf)

            surf.blit(font.render(str(round(Time.fps)), False, (0, 255, 0)), (8, 8))
            surf.blit(font.render(str(round(Time.fixed_fps)), False, (0, 255, 0)), (8, 24))
            
            self.window.blit(pygame.transform.scale(surf, self.window.get_size()), (0, 0))
            pygame.display.flip()
            
            Time.update()