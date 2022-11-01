import socket
from threading import Thread
from thread_return import ThreadReturn

MD5_STR = "fcea920f7412b5da7be0cf42b8c93759"
MAX_NUM = 9999999999
IP = '0.0.0.0'
MAX_PACKET = 1024
PORT = 8080
QUEUE_LEN = 10
CHUNK_SIZE = 10000
NUM_THREADS = 4


def handle_connection(client_socket, client_address, start):
    cpu_count = int(client_socket.recv(MAX_PACKET).decode())
    print(cpu_count)
    end = start + CHUNK_SIZE * cpu_count
    client_socket.send(MD5_STR.encode())
    client_socket.send(str(start).encode())
    client_socket.send(str(end).encode())
    request = client_socket.recv(MAX_PACKET).decode()
    print(request)
    return end


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    start = 0
    threads = []
    try:
        server_socket.bind((IP, PORT))
        server_socket.listen(QUEUE_LEN)
        print("Listening for connections on port %d" % PORT)
        while True:
            client_socket, client_address = server_socket.accept()
            for i in range(NUM_THREADS):
                thread = ThreadReturn(target=handle_connection, args=(client_socket, client_address, start))
                thread.start()
                threads.append(thread)
            for thread in threads:
                end = thread.join()
                print(end)
                start = end
    except socket.error as err:
        print("received socket exception -" + str(err))
    finally:
        server_socket.close()


if __name__ == "__main__":
    main()
