import threading
import socket

from ...constants import TIMEOUT, SERVER_PORT
from .ip import Ip
from .network import SELF_IP, NETMASK


class Scanner:
    """Classe qui scanne le réseau pour trouver un serveur ouvert."""

    def __init__(self) -> None:
        """Constructeur."""
        self._threads: set[threading.Thread] = set()
        self._should_stop: bool = False

    def start(self) -> None:
        """Commencer à scanner le réseau."""
        self._should_stop: bool = False

        scan_thread = threading.Thread(target=self._scan_all)
        scan_thread.start()
        self._threads.add(scan_thread)

    def stop(self) -> None:
        """Arrêter de force le scan."""
        self._should_stop: bool = True

        for thread in self._threads:
            thread.join()
        self._threads.clear()
    
    def _scan_all(self) -> None:
        """Scanner tout le réseau."""

        # Récupérer l'ip et le masque de sous réseau
        net_ip = Ip.from_dec_str(SELF_IP)
        netmask = Ip.from_dec_str(NETMASK)

        # L'ip maximale et minimal
        ip = Ip.min_of_net(net_ip, netmask)
        last_ip = Ip.max_of_net(net_ip, netmask)

        while ip.id < last_ip.id and not self._should_stop:
            try_connect_thread = threading.Thread(
                target=self._try_connect,
                args=(ip.dec_repr_str,)
            )
            try_connect_thread.start()
            self._threads.add(try_connect_thread)

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
            #sock.send("Hello world!\0".encode())
            print(f"[SCANNER] Connected to {ip}")
        
        except (ConnectionRefusedError, TimeoutError):
            pass
        
        sock.close()