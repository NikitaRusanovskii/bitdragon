from network import Peer
from network import Client
from core.metabuilder import Builder
from core.metareader import Reader

def solo_test():
    name = input('> input name: ')
    #peer = Peer()

    my_port = int(input('> input your port: '))
    port = int(input('> input friend port: '))

    client = Client(('127.0.0.1', my_port), name, {'friend': ('127.0.0.1', port)})
    client.start()

def test_with_friend():
    name = input('> input name: ')
    peer = Peer()

    ip = input('> input friend ip: ')
    port = int(input('> input friend port: '))

    client = Client(peer.get_addr(), name, {'friend': (ip, port)})

    client.start()

def build():
    b = Builder(('127.0.0.1', 50000), 1000000001)
    b.create('.\\tests\\test_file.txt', 256)
    b.update()

    r = Reader(r'C:\Users\admin\Desktop\bitdragon\2f0300bae9674026.bit')
    print(r.read())

def main():
    solo_test()

    
        

if __name__ == '__main__':
    main()