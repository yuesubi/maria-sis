"""Le menu d'attente pour se connecter."""

import pyray as pr

from ...utils import Vec2
from ..managers import Scene, SceneId
from .widgets import Anchor, Fit, Frame, Text, TextButton


class WaitMenuScene(Scene):
    """Le menu d'attente pour se connecter."""

    def __init__(self) -> None:
        super().__init__()

        self.main_frame: Frame = Frame(
            Vec2(0, 0), Anchor.NW,
            Vec2.null, Fit.NONE,
            children=[
                Text(
                    Vec2(15, 15), Anchor.NW,
                    "Salle d'attente",
                    pr.Color(0, 0, 0, 255),
                    font_size=30
                ),
                Text(
                    Vec2(15, -15), Anchor.SW,
                    "192.168.1.49:55555",
                    pr.Color(0, 0, 0, 255),
                    font_size=20
                ),
                TextButton(
                    Vec2(-130, -15), Anchor.SE,
                    Vec2(100, 40), Fit.NONE,
                    "QUITTER", pr.Color(0, 0, 0, 255), 16,
                    background_color=pr.Color(200, 100, 200, 255),
                    border_color=pr.Color(255, 100, 255, 255), border_width=3,
                    command=lambda: Scene.pop_scene()
                ),
                TextButton(
                    Vec2(-15, -15), Anchor.SE,
                    Vec2(100, 40), Fit.NONE,
                    "JOUER", pr.Color(0, 0, 0, 255), 16,
                    background_color=pr.Color(200, 100, 200, 255),
                    border_color=pr.Color(255, 100, 255, 255), border_width=3,
                    command=lambda: Scene.pop_scene()
                )
            ] + [
                Text(
                    Vec2(15, 55 + 25*i), Anchor.NW,
                    f"- Joueur n°{i + 1}",
                    pr.Color(0, 0, 0, 255),
                    font_size=20
                )
                for i in range(5)
            ]
        )

    def update(self) -> None:
        self.main_frame.update()

    def render(self) -> None:
        self.main_frame.size.xy = pr.get_screen_width(), pr.get_screen_height()
        self.main_frame.render()