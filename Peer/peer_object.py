import stun


class Peer:
    def __init__(self):
        result = stun.get_ip_info()
        if result[2] and len(result) == 3:
            nat_type, self.external_ip, self.external_port = result
            print('[!] Successful [!]')