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
        own_id = f"{SELF_IP}:{GAME_SERVER_PORT}"
        client_ids = set(map(
            lambda ip: f"{ip}:{GAME_CLIENT_PORT}",
            client_ips
        ))
        all_ids = client_ids.copy()
        all_ids.add(own_id)

        players = { id: Player() for id in all_ids }
        main_player = players[own_id]

        super().__init__(set(players.values()), main_player)

        self.players: dict[str, Player] = players
        
        self.client_ids: set[str] = client_ids
        self.all_ids: set[str] = all_ids
        self.own_id: str = own_id

        self.inputs: dict[str, Player.Inputs] = {
            id: Player.Inputs() for id in self.all_ids
        }

        self.socket: socket.socket = \
            socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((SELF_IP, GAME_SERVER_PORT))
        self.socket.setblocking(False)
    
    def update(self) -> None:
        super().update()

        if pr.is_key_pressed(pr.KeyboardKey.KEY_ESCAPE):
            self.is_pause_menu_open = not self.is_pause_menu_open

        inputs = Player.Inputs()
        if not self.is_pause_menu_open:
            inputs.pressing_left = pr.is_key_down(pr.KeyboardKey.KEY_LEFT)
            inputs.pressing_right = pr.is_key_down(pr.KeyboardKey.KEY_RIGHT)
            inputs.pressing_jump = pr.is_key_down(pr.KeyboardKey.KEY_SPACE)
        self.inputs[self.own_id] = inputs
        
        all_received = False
        while not all_received:
            try:
                data, addr = self.socket.recvfrom(PACKET_SIZE)

                client_id = f"{addr[0]}:{GAME_CLIENT_PORT}"
                msg = data.rstrip(b'\0').decode()

                # TODO: On all packets, add a number, in case the packets are
                #       received in a different order. So that you know if it's
                #       the most up to date packet.

                if len(msg) > 3:
                    inputs = Player.Inputs()
                    inputs.pressing_left = msg[0] == '1'
                    inputs.pressing_right = msg[1] == '1'
                    inputs.pressing_jump = msg[2] == '1'
                    self.inputs[client_id] = inputs
            
            except BlockingIOError:
                all_received = True

        for client_id in self.all_ids:
            player = self.players[client_id]
            player.update(self.inputs[client_id])

            data = (
                f"{client_id}|{player.position.x}|{player.position.y}"
            ).encode()
            data += b'\0' * (PACKET_SIZE - len(data))

            for dest_ip in self.client_ids:
                real_dest_ip = dest_ip.split(':')[0]
                self.socket.sendto(data, (real_dest_ip, GAME_CLIENT_PORT))