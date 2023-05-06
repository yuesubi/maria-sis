import socket
import threading

from ...constants import PACKET_SIZE, SERVER_PORT, TIMEOUT
from .network import SELF_IP


class ScanListener:

    def __init__(self) -> None:
        self._should_stop: bool = False
        self._threads: set[threading.Thread] = set()

    def start(self) -> None:
        self._should_stop = False

        listen_thread = threading.Thread(target=self._listen)
        listen_thread.start()
        self._threads.add(listen_thread)

    def stop(self) -> None:
        self._should_stop = True

        for thread in self._threads:
            thread.join()
        self._threads.clear()

    def _listen(self) -> None:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(TIMEOUT)
        
        addr = SELF_IP, SERVER_PORT
        sock.bind(addr)
        sock.listen()
        print(f"[SCAN LISTENER] Listening on {addr[0]}:{addr[1]}")
        
        while not self._should_stop:
            try:
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
        print(f"[SCAN LISTENER] {client_ip} connected")

        client.settimeout(TIMEOUT)
        
        client_connected = True
        while client_connected and not self._should_stop:
            try:
                msg = client.recv(PACKET_SIZE).decode()
                print(f"[SCAN LISTENER] {client_ip} sent {msg}")

                if msg == "":
                    print(f"[SCAN LISTENER] {client_ip} disconnected")
                    client_connected = False
            
            except TimeoutError:
                pass
        
        try:
            self._threads.remove(threading.current_thread())
        except KeyError:
            pass