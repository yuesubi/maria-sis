import netifaces
import socket
import threading
import typing


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


if __name__ == "__main__":
    PORT = 34678
    SIZE = 1024
    
    print(netifaces.interfaces())
    for interf in netifaces.interfaces():
        # print(netifaces.ifaddresses(interf))
        addr_info = netifaces.ifaddresses(interf).get(netifaces.AF_INET)[0]

        ip = addr_info.get("addr")
        netmask = addr_info.get("netmask")
        print(ip)
        print(netmask)
        print("".join([bin(int(num))[2:] for num in netmask.split(".")]).find("0"))
    """

    msg = "Hello world!".encode()
    
    for ip in IpIterator("192.168.0.44", 24):
        print(f"Sending to {ip}")
        send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        send_sock.sendto(msg + b" " * (SIZE - len(msg)), (ip, PORT))
    
    recv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    recv_sock.bind(("0.0.0.0", PORT))
    recv_sock.settimeout(1)

    while True:
        try:
            msg, addr = recv_sock.recvfrom(SIZE)
            print(f"Received {msg} from {addr}")
        except TimeoutError:
            break
    """