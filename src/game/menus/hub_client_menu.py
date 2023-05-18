"""Le menu d'attente pour se connecter (client)."""

import pyray as pr

from ...utils import Vec2
from ..managers import Scene, SceneId
from ..networking import HubClient
from .widgets import Anchor, Fit, Frame, Text, TextButton


class HubClientMenuScene(Scene):
    """Le menu d'attente pour se connecter (client)."""

    def __init__(self, server_ip: str) -> None:
        """
        Constructeur.
        :param server_ip: L'ip du server qui gère la salle d'attente.
        """
        super().__init__()

        self.hub_client: HubClient = HubClient(server_ip)
        self.hub_client.play_cbk = self.play_callback
        self.hub_client.start()

        self.server_ip: str = server_ip

        self.should_start: bool = False

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
                    command=lambda: Scene.switch_scene(SceneId.SCAN_MENU)
                )
            ]
        )
    
    def quit(self) -> None:
        self.hub_client.stop()

    def update(self) -> None:
        self.main_frame.update()

        if self.should_start:
            Scene.switch_scene(
                SceneId.CLIENT_MULTIPLE_LEVEL,
                self.server_ip,
                self.hub_client.other_clients_ips
            )

    def render(self) -> None:
        self.main_frame.size.xy = pr.get_screen_width(), pr.get_screen_height()
        self.main_frame.render()
    
    def play_callback(self) -> None:
        """Fonction appelé pour commencer à jouer."""
        self.should_start = True