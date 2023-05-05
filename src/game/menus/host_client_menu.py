"""Le menu de choix pour être l'hôte ou le client."""

import pyray as pr

from ...utils import Vec2
from ..managers import Scene, SceneId
from .widgets import Anchor, Fit, Frame, Text, TextButton


class HostClientMenuScene(Scene):
    """Le menu de choix pour être l'hôte ou le client."""

    def __init__(self) -> None:
        super().__init__()

        self.main_frame: Frame = Frame(
            Vec2(0, 0), Anchor.NW,
            Vec2.null, Fit.NONE,
            children=[
                Text(
                    Vec2(0, -100), Anchor.C,
                    "Être l'hôte ou le client ?",
                    pr.Color(0, 0, 0, 255),
                    font_size=30
                ),
                TextButton(
                    Vec2(0, -25), Anchor.C,
                    Vec2(150, 50), Fit.NONE,
                    "HÔTE", pr.Color(0, 0, 0, 255), 20,
                    background_color=pr.Color(200, 100, 200, 255),
                    border_color=pr.Color(255, 100, 255, 255), border_width=3,
                    command=lambda: Scene.push_scene(SceneId.HOST_WAIT_MENU)
                ),
                TextButton(
                    Vec2(0, 40), Anchor.C,
                    Vec2(150, 50), Fit.NONE,
                    "CLIENT", pr.Color(0, 0, 0, 255), 20,
                    background_color=pr.Color(200, 100, 200, 255),
                    border_color=pr.Color(255, 100, 255, 255), border_width=3,
                    command=lambda: Scene.push_scene(SceneId.CONNECT_METHOD_MENU)
                ),
                TextButton(
                    Vec2(0, 100), Anchor.C,
                    Vec2(100, 40), Fit.NONE,
                    "RETOUR", pr.Color(0, 0, 0, 255), 16,
                    background_color=pr.Color(200, 100, 200, 255),
                    border_color=pr.Color(255, 100, 255, 255), border_width=3,
                    command=lambda: Scene.pop_scene()
                )
            ]
        )
    
    def update(self) -> None:
        self.main_frame.update()

    def render(self) -> None:
        self.main_frame.size.xy = pr.get_screen_width(), pr.get_screen_height()
        self.main_frame.render()