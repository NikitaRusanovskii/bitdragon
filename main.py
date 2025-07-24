from network import Peer
from network import Client

def main():

    '''name = input('> input name: ')
    #peer = Peer()

    my_port = int(input('> input your port: '))
    port = int(input('> input friend port: '))

    client = Client(('127.0.0.1', my_port), name, {'friend': ('127.0.0.1', port)})'''

    name = input('> input name: ')
    peer = Peer()

    ip = input('> input friend ip: ')
    port = int(input('> input friend port: '))

    client = Client(peer.get_addr(), name, {'friend': (ip, port)})

    client.start()
    
        

if __name__ == '__main__':
    main()