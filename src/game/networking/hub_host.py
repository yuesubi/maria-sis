import socket
import threading

from ...constants import PACKET_SIZE, HUB_PORT, TIMEOUT
from .network import SELF_IP


class HubHost:

    def __init__(self) -> None:
        """Constructeur."""
        self._should_stop: bool = False
        self._threads: set[threading.Thread] = set()

    def start(self) -> None:
        """Commencer à écouter."""
        self._should_stop = False

        listen_thread = threading.Thread(target=self._listen)
        listen_thread.start()
        self._threads.add(listen_thread)

    def stop(self) -> None:
        """Arrêter d'écouter."""
        self._should_stop = True

        for thread in self._threads:
            thread.join()
        self._threads.clear()

    def _listen(self) -> None:

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(TIMEOUT)
        
        addr = SELF_IP, HUB_PORT
        sock.bind(addr)
        sock.listen()
        print(f"[HUB HOST] Listening on {addr[0]}:{addr[1]}")
        
        while not self._should_stop:
            try:
                # Accepter un client
                client_sock, client_addr = sock.accept()

                handle_thread = threading.Thread(
                    target=self._handle_client,
                    args=(client_sock, client_addr[0])
                )
                handle_thread.start()
                self._threads.add(handle_thread)

            except TimeoutError:
                pass
        
    def _handle_client(self, client: socket.socket, client_ip: str) -> None:
        """
        Prendre en charge un client.
        :param client: Le socket du client.
        :param client_ip: L'adresse ip du client.
        """
        print(f"[HUB HOST] {client_ip} connected")

        client.settimeout(TIMEOUT)

        client_connected = True
        while client_connected and not self._should_stop:
            try:
                msg = client.recv(PACKET_SIZE).rstrip(b'\0').decode()
                # TODO : Plutôt envoyer des message qu'en recevoir

                if msg == "":
                    print(f"[HUB HOST] {client_ip} disconnected")
                    client_connected = False

            except TimeoutError:
                pass
        
        try:
            self._threads.remove(threading.current_thread())
        except KeyError:
            pass