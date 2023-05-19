import itertools
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
        
        self.client_ips: set[str] = set(map(
            lambda ip: f"{ip}:{GAME_CLIENT_PORT}",
            client_ips
        ))
        self.all_ips: set[str] = self.client_ips.copy()
        self.own_ip: str = f"{SELF_IP}:{GAME_SERVER_PORT}"
        self.all_ips.add(self.own_ip)

        self.players: dict[str, Player] = {
            ip: Player() for ip in self.all_ips
        }
        self.inputs: dict[str, Player.Inputs] = {
            ip: Player.Inputs() for ip in self.all_ips
        }

        self.player: Player = self.players[self.own_ip]

        self.level: Level = Level(set(self.players.values()), map_path)

        self.camera: Camera = Camera()
        self.camera.position = self.level.level_map.spawn_point.copy

        self.socket: socket.socket = \
            socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((SELF_IP, GAME_SERVER_PORT))
        self.socket.setblocking(False)
    
    def fixed_update(self) -> None:
        if self.level.winner is None:
            self.level.fixed_update()
            
            self.camera.position = self.camera.position.lerp(
                self.player.position + CAMERA_OFFSET,
                Time.fixed_delta_time * 4
            )
        else:
            self.camera.position = self.camera.position.lerp(
                self.level.winner.position + CAMERA_OFFSET,
                Time.fixed_delta_time
            )

        self.camera.position.x = min(max(
            self.camera.position.x,
            self.level.level_map.top_left.x + WIDTH_IN_BLOCKS/2 - 0.5),
            self.level.level_map.bottom_right.x - WIDTH_IN_BLOCKS/2 - 0.5
        )
        self.camera.position.y = min(max(
            self.camera.position.y,
            self.level.level_map.top_left.y + HEIGHT_IN_BLOCKS/2 - 0.5),
            self.level.level_map.bottom_right.y - HEIGHT_IN_BLOCKS/2 - 0.5
        )
    
    def update(self) -> None:
        inputs = Player.Inputs()
        inputs.pressing_left = pr.is_key_down(pr.KeyboardKey.KEY_LEFT)
        inputs.pressing_right = pr.is_key_down(pr.KeyboardKey.KEY_RIGHT)
        inputs.pressing_jump = pr.is_key_down(pr.KeyboardKey.KEY_SPACE)
        self.inputs[self.own_ip] = inputs
        
        all_received = False
        while not all_received:
            try:
                data, addr = self.socket.recvfrom(PACKET_SIZE)

                ip = f"{addr[0]}:{GAME_CLIENT_PORT}"
                msg = data.rstrip(b'\0').decode()

                # TODO: On all packets, add a number, in case the packets are
                #       received in a different order. So that you know if it's
                #       the most up to date packet.

                if len(msg) > 3:
                    inputs = Player.Inputs()
                    inputs.pressing_left = msg[0] == '1'
                    inputs.pressing_right = msg[1] == '1'
                    inputs.pressing_jump = msg[2] == '1'
                    self.inputs[ip] = inputs
            
            except BlockingIOError:
                all_received = True

        for ip in self.all_ips:
            player = self.players[ip]
            player.update(self.inputs[ip])

            data = (
                f"{ip}|{player.position.x}|{player.position.y}"
            ).encode()
            data += b'\0' * (PACKET_SIZE - len(data))

            for dest_ip in self.client_ips:
                real_dest_ip = dest_ip.split(':')[0]
                self.socket.sendto(data, (real_dest_ip, GAME_CLIENT_PORT))
    
    def render(self) -> None:
        self.camera.begin_render()
        
        for block in self.level.level_map.near_blocks(self.camera.position):
            block.draw(self.camera)
            
        for entity in self.level.entities:
            entity.draw(self.camera)
            
        self.camera.end_render()