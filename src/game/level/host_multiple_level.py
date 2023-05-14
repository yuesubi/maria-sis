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
        
        data = "@"
        while len(data) > 0:
            data, addr = self.socket.recvfrom(PACKET_SIZE)
            ip = addr[0]

            inputs = Player.Inputs()
            inputs.pressing_left = False
            inputs.pressing_right = pr.is_key_down(pr.KeyboardKey.KEY_RIGHT)
            inputs.pressing_jump = pr.is_key_down(pr.KeyboardKey.KEY_SPACE)

            self.inputs[ip] = inputs

        for client_ip in self.client_ips:
            self.players[client_ip].update(self.inputs[client_ip])

            data = ""
            self.socket.sendto(
                data + b' ' * (PACKET_SIZE - len(data)),
                (client_ip, GAME_SERVER_PORT)
            )
    
    def render(self) -> None:
        self.camera.begin_render()
        
        for block in self.level.level_map.near_blocks(self.camera.position):
            block.draw(self.camera)
            
        for entity in self.level.entities:
            entity.draw(self.camera)
            
        self.camera.end_render()