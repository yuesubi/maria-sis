import pyray as pr
import socket

from ...constants import *
from ..level import Player
from ..networking import SELF_IP
from .level_scene import LevelScene


class ClientMultipleLevelScene(LevelScene):
    """L'hôte d'un niveau multijoueur."""

    def __init__(self, server_ip: str, clients_ips: set[str]) -> None:
        """
        Constructeur.
        :param server_ip: L'ip du server qui hôte le jeu.
        :param clients_ips: Les ip des clients.
        """
        players = { f"{ip}:{GAME_CLIENT_PORT}": Player() for ip in clients_ips }
        players[f"{server_ip}:{GAME_SERVER_PORT}"] = Player()

        own_id = f"{SELF_IP}:{GAME_CLIENT_PORT}"
        main_player = players[own_id]

        super().__init__(set(players.values()), main_player)

        self.players: dict[str, Player] = players

        self.own_id: str = own_id
        self.server_ip: str = server_ip

        self.socket: socket.socket = \
            socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((SELF_IP, GAME_CLIENT_PORT))
        self.socket.setblocking(False)
    
    def fixed_update(self) -> None:
        return super().fixed_update(should_update_level=False)

    def update(self) -> None:
        super().update()

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
                player_id = player_pos[0]

                player = self.players[player_id]
                player.position.x = float(player_pos[1])
                player.position.y = float(player_pos[2])
            
            except BlockingIOError:
                all_received = True