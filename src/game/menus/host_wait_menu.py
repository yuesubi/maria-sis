"""Le menu d'attente pour se connecter."""

import pyray as pr
import socket
import threading

from ...constants import SERVER_PORT
from ...utils import Vec2
from ..managers import Scene, SceneId
from .widgets import Anchor, Fit, Frame, Text, TextButton


class ClientData:
    def __init__(
        self,
        name: str,
        addr: tuple[str, int],
        sock: socket.socket,
        thrd: threading.Thread,
        text: Text
    ) -> None:
        self.name: str = name
        self.addr: tuple[str, int] = addr
        self.sock: socket.socket = sock
        self.thrd: threading.Thread = thrd
        self.text: Text = text


class HostWaitMenuScene(Scene):
    """Le menu d'attente pour se connecter."""

    def __init__(self) -> None:
        super().__init__()

        self.accept_running: bool = True
        
        self.accept_thread: threading.Thread = \
            threading.Thread(target=self.wait_for_connection)
        self.accept_thread.start()

        # Clients
        self.clients: list[ClientData] = []
        
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
            ]
        )
    
    def quit(self) -> None:
        self.accept_running = False
        self.accept_thread.join()

    def update(self) -> None:
        self.main_frame.update()

    def render(self) -> None:
        self.main_frame.size.xy = pr.get_screen_width(), pr.get_screen_height()
        self.main_frame.render()
    
    def wait_for_connection(self) -> None:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        
        ADDR = "192.168.1.49", SERVER_PORT
        sock.bind(ADDR)

        sock.listen()
        
        self.accept_running = True
        while self.accept_running:
            try:
                client_sock, client_addr = sock.accept()

                threading.Thread(
                    target=self.handle_client,
                    args=(client_sock, client_addr)
                ).start()

            except TimeoutError:
                pass
        
    def handle_client(self, sock: socket.socket, addr: tuple[str, int]
            ) -> None:
        
        print(f"Client connected : {addr}")
        
        name = sock.recv(1024).decode().split("\0")[0]
        
        text = Text(
            Vec2(15, 55 + 25*len(self.clients)), Anchor.NW,
            f"- {name}",
            pr.Color(0, 0, 0, 255),
            font_size=20
        )
        self.main_frame.add_child(text)
        
        client_data = ClientData(
            name,
            addr, sock,
            threading.current_thread(), text
        )
        self.clients.append(client_data)