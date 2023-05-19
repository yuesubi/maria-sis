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

    def __init__(self, server_ip: str, clients_ips: set[str]) -> None:
        """
        Constructeur.
        :param server_ip: L'ip du server qui hôte le jeu.
        :param clients_ips: Les ip des clients.
        """
        super().__init__()

        map_path = os.path.join(os.path.dirname(__file__),
            "..", "..", "..", "maps", "sample.png")
        
        self.players: dict[str, Player] = {
            f"{ip}:{GAME_CLIENT_PORT}": Player() for ip in clients_ips }
        self.players[f"{server_ip}:{GAME_SERVER_PORT}"] = Player()

        self.own_ip: str = f"{SELF_IP}:{GAME_CLIENT_PORT}"
        self.player: Player = self.players[self.own_ip]

        self.level: Level = Level(set(self.players.values()), map_path)
        
        self.camera: Camera = Camera()
        self.camera.position = self.level.level_map.spawn_point.copy

        self.server_ip: str = server_ip

        self.socket: socket.socket = \
            socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((SELF_IP, GAME_CLIENT_PORT))
        self.socket.setblocking(False)
    
    def fixed_update(self) -> None:
        self.camera.position = self.camera.position.lerp(
            self.player.position + CAMERA_OFFSET,
            Time.fixed_delta_time * 4
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

        msg = ('1' if inputs.pressing_left else '0') + \
            ('1' if inputs.pressing_right else '0') + \
            ('1' if inputs.pressing_jump else '0') + "0"
        data = msg.encode()
        data += b'\0' * (PACKET_SIZE - len(data))

        self.socket.sendto(data, (self.server_ip, GAME_SERVER_PORT))

        # Pump packets
        all_received = False
        while not all_received:
            try:
                data, _ = self.socket.recvfrom(PACKET_SIZE)

                # TODO: Check if the message actually comes from the sever, and
                #       not some random computer.

                player_pos = data.rstrip(b'\0').decode().split('|')
                ip = player_pos[0]

                player = self.players[ip]
                player.position.x = float(player_pos[1])
                player.position.y = float(player_pos[2])
            
            except BlockingIOError:
                all_received = True
    
    def render(self) -> None:
        self.camera.begin_render()
        
        for block in self.level.level_map.near_blocks(self.camera.position):
            block.draw(self.camera)
            
        for entity in self.level.entities:
            entity.draw(self.camera)
            
        self.camera.end_render()