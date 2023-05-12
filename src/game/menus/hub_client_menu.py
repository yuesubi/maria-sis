"""Le menu d'attente pour se connecter (client)."""

import pyray as pr

from ...utils import Vec2
from ..managers import Scene, SceneId
from ..networking import HubHost, ScanListener
from .widgets import Anchor, Fit, Frame, Text, TextButton


class HubClientMenuScene(Scene):
    """Le menu d'attente pour se connecter (client)."""

    def __init__(self, server_ip: str) -> None:
        """
        Constructeur.
        :param server_ip: L'ip du server qui gère la salle d'attente.
        """
        super().__init__()

        # TODO: Add hub client & start

        self.server_ip: str = server_ip

        # Interface graphique
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
                    f"{server_ip}",
                    pr.Color(0, 0, 0, 255),
                    font_size=20
                ),
                TextButton(
                    Vec2(-15, -15), Anchor.SE,
                    Vec2(100, 40), Fit.NONE,
                    "QUITTER", pr.Color(0, 0, 0, 255), 16,
                    background_color=pr.Color(200, 100, 200, 255),
                    border_color=pr.Color(255, 100, 255, 255), border_width=3,
                    command=lambda: Scene.pop_scene()
                )
            ]
        )
    
    def quit(self) -> None:
        pass

    def update(self) -> None:
        self.main_frame.update()

    def render(self) -> None:
        self.main_frame.size.xy = pr.get_screen_width(), pr.get_screen_height()
        self.main_frame.render()