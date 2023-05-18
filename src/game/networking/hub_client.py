import socket
import threading
import time
from typing import Callable

from ...constants import *


class HubClient:
    """Classe qui scanne le réseau pour trouver un serveur ouvert."""

    def __init__(self, server_ip: str) -> None:
        """Constructeur."""

        self._server_ip: str = server_ip
        self._other_clients_ips: set[str] = set()
        self._other_clients_ips_lock: threading.Lock = threading.Lock()
        
        self.conn_cbk: Callable[[], None] | None = None
        self.dconn_cbk: Callable[[], None] | None = None
        self.play_cbk: Callable[[], None] | None = None

        self._loop_threat: threading.Thread | None = None
        self._should_stop: bool = True
    
    @property
    def other_clients_ips(self) -> set[str]:
        """Assesseur des ips """
        self._other_clients_ips_lock.acquire()
        other_clients_ips = self._other_clients_ips.copy()
        self._other_clients_ips_lock.release()
        return other_clients_ips

    def start(self) -> None:
        """Commencer à scanner le réseau."""
        print("[HUB CLIENT] Starting")
        self._should_stop = False

        self._loop_threat = threading.Thread(target=self._connect)
        self._loop_threat.start()

    def stop(self) -> None:
        """Arrêter de force le scan."""
        print("[HUB CLIENT] Stopping")
        self._should_stop = True

        if self._loop_threat is not None:
            self._loop_threat.join()
            self._loop_threat = None
        
    def _connect(self) -> None:
        """Se connecter au server."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(TIMEOUT)

        sock.connect((self._server_ip, HUB_PORT))

        print(f"[HUB CLIENT] Connected to {self._server_ip}")

        if self.conn_cbk is not None:
            self.conn_cbk()

        while not self._should_stop:
            try:
                msg = sock.recv(PACKET_SIZE).rstrip(b'\0').decode()
                print(f"[HUB CLIENT] Recv \"{msg}\"")

                info = msg.split('|')

                if msg == "":
                    self._should_stop = True
                elif info[0] == "!play":
                    self.play_cbk()
                elif info[0] == "!ips":
                    self._other_clients_ips_lock.acquire()
                    self._other_clients_ips = set(info[1:])
                    self._other_clients_ips_lock.release()
            
            except TimeoutError:
                pass
    
        if self.dconn_cbk is not None:
            self.dconn_cbk()

        sock.close()