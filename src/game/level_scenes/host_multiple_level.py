import pyray as pr
import socket

from ...constants import *
from ..level import Player
from ..managers import Time, Scene
from ..networking import SELF_IP
from .level_scene import LevelScene


class HostMultipleLevelScene(LevelScene):
    """L'hôte d'un niveau multijoueur."""

    def __init__(self, client_ips: set[str]) -> None:
        """
        Constructeur.
        :param client_ips: Les ips des clients.
        """
        own_ip = f"{SELF_IP}:{GAME_SERVER_PORT}"
        client_ips = set(map(
            lambda ip: f"{ip}:{GAME_CLIENT_PORT}",
            client_ips
        ))
        all_ips = client_ips.copy()
        all_ips.add(own_ip)

        players = { ip: Player() for ip in all_ips }
        main_player = players[own_ip]

        super().__init__(set(players.values()), main_player)

        self.players: dict[str, Player] = players
        
        self.client_ips: set[str] = client_ips
        self.all_ips: set[str] = all_ips
        self.own_ip: str = own_ip

        self.inputs: dict[str, Player.Inputs] = {
            ip: Player.Inputs() for ip in self.all_ips
        }

        self.socket: socket.socket = \
            socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((SELF_IP, GAME_SERVER_PORT))
        self.socket.setblocking(False)
    
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