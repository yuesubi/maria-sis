"""Le menu de scan de partie."""

import pyray as pr

from ...constants import SERVER_PORT
from ...utils import Vec2
from ..managers import Scene, SceneId
from ..networking import Scanner
from .widgets import Anchor, Fit, Frame, Text, TextButton


class PartyEntry:
    def __init__(
        self,
        name: str,
        ip: str,
        text: Text
    ) -> None:
        self.name: str = name
        self.ip: str = ip
        self.text: Text = text


class ScanMenuScene(Scene):
    """Le menu de scan de partie."""

    def __init__(self) -> None:
        super().__init__()

        self.scanner: Scanner = Scanner()
        self.scanner.callback = self.add_server_frame

        self.servers: dict[str, Frame] = {}

        self.main_frame: Frame = Frame(
            Vec2(0, 0), Anchor.NW,
            Vec2.null, Fit.NONE,
            children=[
                Text(
                    Vec2(15, 15), Anchor.NW,
                    "Scanner",
                    pr.Color(0, 0, 0, 255),
                    font_size=30
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
                    "SCANNER", pr.Color(0, 0, 0, 255), 16,
                    background_color=pr.Color(200, 100, 200, 255),
                    border_color=pr.Color(255, 100, 255, 255), border_width=3,
                    command=lambda: (self.scanner.stop(), self.scanner.start())
                )
            ]
        )
    
    def quit(self) -> None:
        self.scanner.stop()

    def update(self) -> None:
        self.main_frame.update()

        ips_to_del = set()
        for ip, frame in self.servers.items():
            if not self.scanner.is_connected(ip):
                print(ip)
                self.main_frame.remove_child(frame)
                ips_to_del.add(ip)
        for ip in ips_to_del:
            del self.servers[ip]


    def render(self) -> None:
        self.main_frame.size.xy = pr.get_screen_width(), pr.get_screen_height()
        self.main_frame.render()
    
    def add_server_frame(self, ip: str) -> None:
        frame = Frame(
            Vec2(15, 55 + 25 * len(self.servers)), Anchor.NW,
            Vec2(250, 20), Fit.NONE,
            children=[
                Text(
                    Vec2(0, 0), Anchor.W,
                    f"- {ip}",
                    pr.Color(0, 0, 0, 255),
                    font_size=20
                ),
                TextButton(
                    Vec2(0, 0), Anchor.E,
                    Vec2(50, 25), Fit.NONE,
                    "-C", pr.Color(0, 0, 0, 255), 16,
                    background_color=pr.Color(200, 100, 200, 255),
                    border_color=pr.Color(255, 100, 255, 255), border_width=3,
                    command=None
                )
            ]
        )

        self.main_frame.add_child(frame)
        self.servers[ip] = frame