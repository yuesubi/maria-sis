import os
import pyray as pr
import socket

from ...constants import *
from ..managers import Time, Scene
from ..networking import SELF_IP
from .camera import Camera
from .entity import Player
from .level import Level


class HostMultipleLevelScene(Scene):
    """L'hôte d'un niveau multijoueur."""

    def __init__(self, client_ips: set[str]) -> None:
        """Constructeur."""
        super().__init__()

        map_path = os.path.join(os.path.dirname(__file__),
            "..", "..", "..", "maps", "sample.png")
        self.player = Player()
        
        self.camera: Camera = Camera()
        self.camera.position = self.level.level_map.spawn_point.copy

        self.client_ips: set[str] = client_ips
        self.players: dict[str, Player] = {
            ip: Player() for ip in self.client_ips
        }
        self.inputs: dict[str, Player.Inputs] = {
            ip: Player.Inputs() for ip in self.client_ips
        }

        self.player: Player = Player()
        self.players[SELF_IP] = self.players

        self.level: Level = Level(set(self.players.values()), map_path)

        self.socket: socket.socket = \
            socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((SELF_IP, GAME_SERVER_PORT))
        self.socket.setblocking(False)
    
    def fixed_update(self) -> None:
        self.level.fixed_update()
        
        self.camera.position = self.camera.position.lerp(
            self.player.position + CAMERA_OFFSET,
            Time.fixed_delta_time * 4
        )

        self.camera.position.x = min(max(
            self.camera.position.x,
            self.level.level_map.top_left.x),
            self.level.level_map.bottom_right.x
        )
        self.camera.position.y = min(max(
            self.camera.position.y,
            self.level.level_map.top_left.y),
            self.level.level_map.bottom_right.y
        )
    
    def update(self) -> None:
        inputs = Player.Inputs()
        inputs.pressing_left = pr.is_key_down(pr.KeyboardKey.KEY_LEFT)
        inputs.pressing_right = pr.is_key_down(pr.KeyboardKey.KEY_RIGHT)
        inputs.pressing_jump = pr.is_key_down(pr.KeyboardKey.KEY_SPACE)
        self.player.update(inputs)
        
        all_received = False
        while not all_received:
            try:
                data, addr = self.socket.recvfrom(PACKET_SIZE)

                ip = addr[0]
                msg = data.rstrip(b'\0').decode()

                # TODO: On all packets, add a number, in case the packets are
                #       received in a different order. So that you know if it's
                #       the most up to date packet.

                inputs = Player.Inputs()
                inputs.pressing_left = msg[0] == '1'
                inputs.pressing_right = msg[1] == '1'
                inputs.pressing_jump = msg[2] == '1'
                self.inputs[ip] = inputs
            
            except BlockingIOError:
                all_received = True

        for client_ip in self.client_ips:
            player = self.players[client_ip]
            player.update(self.inputs[client_ip])

            data = (
                f"{client_ip}|{player.position.x}|{player.position.y}"
            ).encode()
            data += b'\0' * (PACKET_SIZE - len(data))

            for dest_ip in self.client_ips:
                self.socket.sendto(data, (dest_ip, GAME_CLIENT_PORT))
    
    def render(self) -> None:
        self.camera.begin_render()
        
        for block in self.level.level_map.near_blocks(self.camera.position):
            block.draw(self.camera)
            
        for entity in self.level.entities:
            entity.draw(self.camera)
            
        self.camera.end_render()