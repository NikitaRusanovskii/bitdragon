CHUNK_SIZE = 256
TOTAL_CHUNKS = (256*4*1024)//6
FILENAME = 'test_file.txt'

def generate_test_file():
    with open(FILENAME, 'wb') as f:
        for i in range(TOTAL_CHUNKS):
            f.write('aboba\n'.encode())
    print(f'[+] Файл "{FILENAME}" успешно создан. Размер: {CHUNK_SIZE * TOTAL_CHUNKS} байт')

if __name__ == '__main__':
    generate_test_file()
