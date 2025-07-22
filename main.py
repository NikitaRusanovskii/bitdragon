from Peer import Peer
from client import Client

def main():

    name = input('your name: ')

    peer = Peer()
    client = Client(peer.external_ip, peer.external_port)

    friend_ip = input('friend ip: ')
    friend_port = input('friend port: ')

    client.punch(friend_ip=friend_ip, friend_port=friend_port)
    
        

if __name__ == '__main__':
    main()