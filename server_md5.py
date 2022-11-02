import socket
from threading import Thread
from thread_return import ThreadReturn

MD5_STR = "fcea920f7412b5da7be0cf42b8c93759"
MAX_NUM = 9999999999
IP = '0.0.0.0'
MAX_PACKET = 1024
PORT = 8080
QUEUE_LEN = 10
CHUNK_SIZE = 100000
NUM_THREADS = 4
answers_list = []
end = 0
start = 0

#def create_msg()


def handle_connection(client_socket, client_address, start):
    global end
    cpu_count = int(client_socket.recv(MAX_PACKET).decode())
    print(cpu_count)
    end = start + CHUNK_SIZE * cpu_count
    client_socket.send(MD5_STR.encode())
    client_socket.send(str(start).encode())
    client_socket.send(str(end).encode())
    answer = client_socket.recv(MAX_PACKET).decode()
    print(answer)
    answers_list.append(answer + str(end))


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    threads = []
    answer = -1
    global start
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
                answer += 1
            for thread in threads:
                thread.join()
                start = end
                print(start)
    except socket.error as err:
        print("received socket exception -" + str(err))
    finally:
        server_socket.close()


if __name__ == "__main__":
    main()
