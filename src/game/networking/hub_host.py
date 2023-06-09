import socket
import threading
import time

from ...constants import PACKET_SIZE, HUB_PORT, TIMEOUT
from .network import SELF_IP


class HubHost:

    def __init__(self) -> None:
        """Constructeur."""
        self._threads: set[threading.Thread] = set()
        self._threads_lock: threading.Lock = threading.Lock()

        self._ips: set[str] = set()
        self._ips_lock: threading.Lock = threading.Lock()

        self._should_stop: bool = False
        self._should_send_play_msg: bool = False
    
    @property
    def ips(self) -> set[str]:
        self._ips_lock.acquire()
        ips = self._ips.copy()
        self._ips_lock.release()
        return ips

    def start(self) -> None:
        """Commencer à écouter."""
        print(f"[HUB HOST] Starting")
        self._should_stop = False

        listen_thread = threading.Thread(target=self._listen)
        listen_thread.start()

        self._threads_lock.acquire()
        self._threads.add(listen_thread)
        self._threads_lock.release()
    
    def send_play_msg(self) -> None:
        """Dire au clients qu'il faut commencer la partie."""
        self._should_send_play_msg = True

    def stop(self) -> None:
        """Arrêter d'écouter."""
        print(f"[HUB HOST] Stopping")
        self._should_stop = True

        self._threads_lock.acquire()
        for thread in self._threads:
            thread.join()
        self._threads.clear()
        self._threads_lock.release()

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

                if self._threads_lock.acquire(blocking=False):
                    handle_thread.start()
                    self._threads.add(handle_thread)
                    self._threads_lock.release()

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

        self._ips_lock.acquire()
        self._ips.add(client_ip)
        self._ips_lock.release()

        has_sent_play_msg = False

        try:
            while (not self._should_stop) or \
                    (has_sent_play_msg != self._should_send_play_msg):
                
                # try:
                #     msg = client.recv(PACKET_SIZE).rstrip(b'\0').decode()
                # except TimeoutError:
                #     pass

                msg = str()
                if has_sent_play_msg != self._should_send_play_msg:
                    msg = "!play"
                    has_sent_play_msg = True
                else:
                    self._ips_lock.acquire()
                    msg = "!ips|" + '|'.join(self._ips)
                    self._ips_lock.release()
                
                data = msg.encode()
                data += b'\0' * (PACKET_SIZE - len(data))
                client.send(data)

                time.sleep(0.5)
        
        except (BrokenPipeError, ConnectionResetError):
            print(f"[HUB HOST] {client_ip} disconnected")

        if not self._should_send_play_msg:
            self._ips_lock.acquire()
            self._ips.remove(client_ip)
            self._ips_lock.release()
        
        if self._threads_lock.acquire(blocking=False):
            self._threads.remove(threading.current_thread())
            self._threads_lock.release()