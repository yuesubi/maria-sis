import netifaces


def find_ip_and_netmask() -> tuple[str, str]:
    addr = "0.0.0.0", "255.255.255.255"

    for iface in netifaces.interfaces():
        ipv4_infos = netifaces.ifaddresses(iface).get(netifaces.AF_INET)

        if ipv4_infos is not None:
            for ipv4 in ipv4_infos: 
                ip = ipv4["addr"]
                net_mask = ipv4["mask"]

                # Si l'adresse n'est pas le loopback device
                if ip != "127.0.0.1":
                    addr = ip, net_mask
    
    return addr


_addr = find_ip_and_netmask()
SELF_IP: str = _addr[0]
NETMASK: str = _addr[1]