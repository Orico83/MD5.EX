import hashlib
import socket
from os import cpu_count
from threading import Thread

SERVER_IP = '127.0.0.1'
PORT = 8820
MAX_PACKET = 1024
CHUNK_SIZE = 100000
ORIGINAL_LEN = 8
answer = "NOT FOUND"
free_cpus = cpu_count()
threads = []
start = 0
starts = 0
ends = 0
found = False


def calculate_password(md5_str, start1, end):
    global answer, found
    print(f"Checking from {start1} to {end}")
    while start1 != end:
        if hashlib.md5(str(start1).zfill(ORIGINAL_LEN).encode()).hexdigest() == md5_str:
            answer = str(start1)
            found = True
        start1 += 1


def main():
    global free_cpus, starts, ends, start, found
    finish = ''
    try:

        while not found:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            client_socket.connect((SERVER_IP, PORT))
            print("Connected to server")
            client_socket.send(str(cpu_count()).encode())
            print("Sent CPU count")
            data = client_socket.recv(1024).decode()
            print("The server sent " + data)
            msg = data.split("$")[0]
            start = int(data.split("$")[1])
            end = int(data.split("$")[2])
            while free_cpus > 0:
                if finish != "DISCONNECT":
                    ends = start + int(end / cpu_count())
                    thread = Thread(target=calculate_password, args=(msg, start, ends))
                    free_cpus -= 1
                    print(f"starting thread number {cpu_count() - free_cpus}...")
                    thread.start()
                    threads.append(thread)
                    if answer != "NOT FOUND":
                        client_socket.send(answer.encode())
                        print("Sent answer:" + answer)
                        finish = client_socket.recv(10).decode()
                        break
                    start += int(end / cpu_count())
            print("waiting for the threads to end...")
            for thread in threads:
                thread.join()
            client_socket.send("NOT FOUND".encode())
            client_socket.recv(MAX_PACKET)
            client_socket.close()
            free_cpus = cpu_count()

    except socket.error as err:
        print(str(err))
        print("disconnecting...")
        exit()
    finally:
        exit()


if __name__ == "__main__":
    main()
