import socket
from threading import Thread

MD5_STR = "25d55ad283aa400af464c76d713c07ad"
IP = '0.0.0.0'
MAX_PACKET = 1024
PORT = 8820
QUEUE_LEN = 10
CHUNK_SIZE = 100000
NUM_THREADS = 4
answers_list = []
threads = []
end = 0
start = 0
cpu_count = 0
answer = "NOT FOUND"
found = False


def create_msg():
    global start
    global end
    end += CHUNK_SIZE * cpu_count
    msg = MD5_STR + "$" + str(start) + "$" + str(end)
    start = end
    return msg


def handle_connection(client_socket):
    global found, end, cpu_count, answer
    num = 0
    try:
        cpu_count = int(client_socket.recv(MAX_PACKET).decode())
        print("Client CPU count: " + str(cpu_count))
        client_socket.send(create_msg().encode())
        num += 1
        print(f"Sent to client number{num}")
        answer = client_socket.recv(MAX_PACKET).decode()
        if answer != "NOT FOUND":
            print("answer: " + answer)
            found = True
            client_socket.send("DISCONNECT".encode())
        else:
            client_socket.send("NOT FOUND!".encode())
    except socket.error as err:
        print(str(err))
    finally:
        """client_socket.close()
        print("Disconnected from client")"""


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
    server_socket.listen(QUEUE_LEN)
    print("Listening for connections on port %d" % PORT)
    global found
    try:
        while not found:
            client_socket, client_address = server_socket.accept()
            print(f"connected to client {client_address}")
            thread = Thread(target=handle_connection, args=(client_socket,))
            thread.start()
            threads.append(thread)
            for thread in threads:
                thread.join()
    except socket.error as err:
        print("received socket exception -" + str(err))
    finally:
        server_socket.close()


if __name__ == "__main__":
    main()