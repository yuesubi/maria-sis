"""La scène principale du jeu."""

import pyray as pr

from ...utils import Vec2
from ..managers import Scene
from .widgets import Anchor, Fit, Frame, Text


class MainMenuScene(Scene):
    """La scène principale du jeu."""

    def __init__(self) -> None:
        super().__init__()

        self.main_frame: Frame = Frame(
            Vec2(0, 0), Anchor.NW,
            Vec2.null, Fit.NONE,
            children=[
                Text(
                    Vec2(0, 0), Anchor.C,
                    "Hello world!",
                    pr.Color(0, 0, 0),
                    font_size=20 
                )
            ]
        )
    
    def update(self) -> None:
        self.main_frame.update()

    def render(self) -> None:
        self.main_frame.size.xy = pr.get_screen_width(), pr.get_screen_height()
        self.main_frame.render()