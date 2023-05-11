import threading
import time
from typing import Callable
import socket

from ...constants import *
from .ip import Ip
from .network import SELF_IP, NETMASK


class Scanner:
    """Classe qui scanne le réseau pour trouver un serveur ouvert."""

    def __init__(self) -> None:
        """Constructeur."""
        self._threads: set[threading.Thread] = set()

        self._run_lock: threading.Lock = threading.Lock()
        self._should_stop: threading.Lock = threading.Lock()

        self.conn_cbk: Callable[[str], None] | None = None
        self.disconn_cbk: Callable[[str], None] | None = None

    def start(self) -> None:
        """Commencer à scanner le réseau."""
        if self._run_lock.locked():
            raise RuntimeError("Can't start two times")
        
        self._run_lock.acquire()

        scan_thread = threading.Thread(target=self._scan_all)
        scan_thread.start()
        self._threads.add(scan_thread)

    def stop(self) -> None:
        """Arrêter de force le scan."""
        if self._run_lock.locked():
            self._should_stop.acquire()

            for thread in self._threads:
                thread.join()
            self._threads.clear()

            self._should_stop.release()
            self._run_lock.release()
        
    def _scan_all(self) -> None:
        """Scanner tout le réseau."""

        # Récupérer l'ip et le masque de sous réseau
        net_ip = Ip.from_dec_str(SELF_IP)
        netmask = Ip.from_dec_str(NETMASK)

        # L'ip maximale et minimal
        ip = Ip.min_of_net(net_ip, netmask)
        last_ip = Ip.max_of_net(net_ip, netmask)

        while ip.id < last_ip.id and not self._should_stop.locked():
            try_connect_thread = threading.Thread(
                target=self._try_connect,
                args=(ip.dec_repr_str,)
            )
            try_connect_thread.start()
            
            if self._should_stop.acquire(blocking=False):
                self._threads.add(try_connect_thread)
                self._should_stop.release()

            ip.id += 1

    def _try_connect(self, ip: str) -> None:
        """
        Tenter d'établir une connection avec une ip.
        :param ip: L'ip à tester.
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(TIMEOUT)

        try:
            sock.connect((ip, SERVER_PORT))
            print(f"[SCANNER] Connected to {ip}")

            # Appeler la fonction de connexion
            if self.conn_cbk is not None:
                self.conn_cbk(ip)

            while not self._should_stop.locked():
                # msg = "!info".encode()
                # sock.send(msg + b'\0' * (PACKET_SIZE - len(msg)))
                time.sleep(WAIT_MENU_REFRESH_INTERVAL)
            
            # Appeler la fonction de déconnexion
            if self.disconn_cbk is not None:
                self.disconn_cbk(ip)
        
        except (ConnectionRefusedError, TimeoutError):
            pass
        
        sock.close()