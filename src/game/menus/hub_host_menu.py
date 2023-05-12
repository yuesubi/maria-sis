"""Le menu d'attente pour se connecter."""

import pyray as pr

from ...constants import SCAN_PORT
from ...utils import Vec2
from ..managers import Scene, SceneId
from ..networking import HubHost, ScanListener, SELF_IP
from .widgets import Anchor, Fit, Frame, Text, TextButton


class HubHostMenuScene(Scene):
    """Le menu d'attente pour se connecter."""

    def __init__(self) -> None:
        super().__init__()

        self.scan_listener: ScanListener = ScanListener()
        self.scan_listener.start()

        self.hub_host: HubHost = HubHost()
        self.hub_host.start()

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
                    f"{SELF_IP}:{SCAN_PORT}",
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
            ]
        )
    
    def quit(self) -> None:
        self.scan_listener.stop()
        self.hub_host.stop()

    def update(self) -> None:
        self.main_frame.update()

    def render(self) -> None:
        self.main_frame.size.xy = pr.get_screen_width(), pr.get_screen_height()
        self.main_frame.render()