"""La scène principale du jeu."""

import pyray as pr

from ...utils import Vec2
from ..managers import Scene, SceneId
from .widgets import Anchor, Fit, Frame, Text, TextButton


class MainMenuScene(Scene):
    """La scène principale du jeu."""

    def __init__(self) -> None:
        super().__init__()

        self.main_frame: Frame = Frame(
            Vec2(0, 0), Anchor.NW,
            Vec2.null, Fit.NONE,
            children=[
                Text(
                    Vec2(0, -100), Anchor.C,
                    "Maria Sis",
                    pr.Color(0, 0, 0, 255),
                    font_size=40
                ),
                TextButton(
                    Vec2(0, 0), Anchor.C,
                    Vec2(150, 50), Fit.NONE,
                    "SOLO", pr.Color(0, 0, 0, 255), 20,
                    background_color=pr.Color(200, 100, 200, 255),
                    border_color=pr.Color(255, 100, 255, 255), border_width=3,
                    command=self.solo_button_cmd
                ),
                TextButton(
                    Vec2(0, 75), Anchor.C,
                    Vec2(150, 50), Fit.NONE,
                    "MULTI", pr.Color(0, 0, 0, 255), 20,
                    background_color=pr.Color(200, 100, 200, 255),
                    border_color=pr.Color(255, 100, 255, 255), border_width=3,
                    command=lambda: print("Multi")
                )
            ]
        )
    
    def update(self) -> None:
        self.main_frame.update()

    def render(self) -> None:
        self.main_frame.size.xy = pr.get_screen_width(), pr.get_screen_height()
        self.main_frame.render()
    
    def solo_button_cmd(self) -> None:
        """Commande du bouton solo."""
        Scene.switch_scene(SceneId.LEVEL)