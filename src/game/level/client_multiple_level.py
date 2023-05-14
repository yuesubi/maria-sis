import os
import pyray as pr
import socket

from ...constants import *
from ..managers import Time, Scene
from ..networking import SELF_IP
from .camera import Camera
from .entity import Player
from .level import Level


class ClientMultipleLevelScene(Scene):
    """L'hôte d'un niveau multijoueur."""

    def __init__(self, server_ip: str) -> None:
        """Constructeur."""
        super().__init__()

        map_path = os.path.join(os.path.dirname(__file__),
            "..", "..", "..", "maps", "sample.png")
        self.player = Player()

        self.level: Level = Level(set([self.player]), map_path)
        
        self.camera: Camera = Camera()
        self.camera.position = self.level.level_map.spawn_point.copy

        self.server_ip: str = server_ip
        self.socket: socket.socket = \
            socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((SELF_IP, GAME_CLIENT_PORT))
    
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

        msg = '1' if inputs.pressing_left else '0' + \
            '1' if inputs.pressing_right else '0' + \
            '1' if inputs.pressing_jump else '0' + "0"
        data = msg.encode()

        self.socket.sendto(
            data + b' ' * (PACKET_SIZE - len(data)),
            (self.server_ip, GAME_SERVER_PORT)
        )

        self.player.update(inputs)
    
    def render(self) -> None:
        self.camera.begin_render()
        
        for block in self.level.level_map.near_blocks(self.camera.position):
            block.draw(self.camera)
            
        for entity in self.level.entities:
            entity.draw(self.camera)
            
        self.camera.end_render()