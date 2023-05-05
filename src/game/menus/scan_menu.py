"""Le menu de scan de partie."""

import netifaces
import pyray as pr
import socket
import threading
import typing

from ...constants import SERVER_PORT
from ...utils import Vec2
from ..managers import Scene, SceneId
from .widgets import Anchor, Fit, Frame, Text, TextButton


class IpIterator(typing.Iterator):
    def __init__(self, net_address: str, net_sub_mask: int) -> None:
        super().__init__()

        dec_addr = [int(number) for number in net_address.split(".")]
        str_addr = "".join(map(
            lambda num_bin: "0" * (8 - len(num_bin)) + num_bin,
            [bin(number)[2:] for number in dec_addr]
        ))

        self._addr_id = sum([
            int(number_str) * (2**i)
            for i, number_str in enumerate(reversed(
                str_addr[:net_sub_mask] + "0" * len(str_addr[net_sub_mask:])
            ))
        ])

        self._end_id = sum([
            int(number_str) * (2**i)
            for i, number_str in enumerate(reversed(
                str_addr[:net_sub_mask] + "1" * len(str_addr[net_sub_mask:])
            ))
        ])
    
    def _id_to_decimal_ip(self, id: int) -> list[int]:
        decimal_ip = list()
        remainder = id
        for _ in range(4):
            decimal_ip.append(remainder % 256)
            remainder //= 256
        return decimal_ip
    
    def __iter__(self) -> 'IpIterator':
        return self
    
    def __next__(self) -> str:
        self._addr_id += 1

        if not (self._addr_id < self._end_id):
            raise StopIteration

        ip = ".".join(map(str, reversed(self._id_to_decimal_ip(self._addr_id))))
        
        return ip


class PartyEntry:
    def __init__(
        self,
        name: str,
        ip: str,
        text: Text
    ) -> None:
        self.name: str = name
        self.ip: str = ip
        self.text: Text = text


class ScanMenuScene(Scene):
    """Le menu de scan de partie."""

    def __init__(self) -> None:
        super().__init__()

        self.parties: list[PartyEntry] = []

        self.main_frame: Frame = Frame(
            Vec2(0, 0), Anchor.NW,
            Vec2.null, Fit.NONE,
            children=[
                Text(
                    Vec2(15, 15), Anchor.NW,
                    "Scanner",
                    pr.Color(0, 0, 0, 255),
                    font_size=30
                ),
                TextButton(
                    Vec2(-130, -15), Anchor.SE,
                    Vec2(100, 40), Fit.NONE,
                    "QUITTER", pr.Color(0, 0, 0, 255), 16,
                    background_color=pr.Color(200, 100, 200, 255),
                    border_color=pr.Color(255, 100, 255, 255), border_width=3,
                    command=lambda: Scene.pop_scene()
                ),
                TextButton(
                    Vec2(-15, -15), Anchor.SE,
                    Vec2(100, 40), Fit.NONE,
                    "SCANNER", pr.Color(0, 0, 0, 255), 16,
                    background_color=pr.Color(200, 100, 200, 255),
                    border_color=pr.Color(255, 100, 255, 255), border_width=3,
                    command=lambda: self.start_scan_all()
                )
            ] + [
                Text(
                    Vec2(15, 55 + 25*i), Anchor.NW,
                    f"- Joueur n°{i + 1}",
                    pr.Color(0, 0, 0, 255),
                    font_size=20
                )
                for i in range(5)
            ]
        )

        self.ip, self.netmask = self.find_ip_and_netmask()

        self.scan_thread: threading.Thread | None = None
        print(f"Self ip : {self.ip}/{self.netmask}")

    def update(self) -> None:
        self.main_frame.update()

    def render(self) -> None:
        self.main_frame.size.xy = pr.get_screen_width(), pr.get_screen_height()
        self.main_frame.render()
    
    def find_ip_and_netmask(self) -> tuple[str, int]:
        ip_addr = "127.0.0.1", 30

        for interf in netifaces.interfaces():
            addr_info = netifaces.ifaddresses(interf).get(netifaces.AF_INET)[0]

            ip = addr_info.get("addr")
            netmask = ("".join([
                bin(int(num))[2:]
                for num in addr_info.get("mask").split(".")
            ]) + "0").find("0")

            if ip != "127.0.0.1":
                ip_addr = ip, netmask
        
        return ip_addr

    def start_scan_all(self) -> None:
        if self.scan_thread is not None:
            if self.scan_thread.is_alive():
                return
        
        self.scan_thread = threading.Thread(
            target=self.scan_all,
            args=(IpIterator(self.ip, self.netmask),)
        )
        self.scan_thread.start()

    def scan_all(self, ip_iterator: IpIterator) -> None:
        for ip in ip_iterator:
            t = threading.Thread(target=self.handle_conn, args=(ip,))
            t.start()

    def handle_conn(self, ip: str) -> None:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)

        try:
            sock.connect((ip, SERVER_PORT))
            sock.send("Hello world!\0".encode())
            print(f"Open conn on {self.ip}")
        except BaseException as err:
            pass #print(err)
        
        sock.close()