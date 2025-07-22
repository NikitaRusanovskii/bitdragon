from Peer import Peer
from client import Client

def main():
    peer = Peer()
    client = Client(peer.external_ip, peer.external_port)

    friend_ip = input()
    friend_port = input()

    client.punch(friend_ip=friend_ip, friend_port=friend_port)
    
        

if __name__ == '__main__':
    main()