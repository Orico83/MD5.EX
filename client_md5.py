import hashlib
import socket
from os import cpu_count
from threading import Thread

SERVER_IP = '127.0.0.1'
PORT = 8820
MAX_PACKET = 1024
CHUNK_SIZE = 100000
ORIGINAL_LEN = 7
answer = "NOT FOUND"
free_cpus = cpu_count()
total_cpu = cpu_count()
threads = []
start = 0
starts = 0
mid = 0
ends = 0


def give_range(start2, end):
    global starts, ends, start
    starts = start2
    ends = starts + CHUNK_SIZE
    start = ends
    return starts, ends


def calculate_password(md5_str, start1, end):
    global answer
    while start1 != end:
        if hashlib.md5(str(start1).zfill(ORIGINAL_LEN).encode()).hexdigest() == md5_str:
            answer = str(start1)
        start1 += 1
    print(answer)


def main():
    global free_cpus, total_cpu, starts, mid, ends, start
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_IP, PORT))
    print("Connected to server")
    try:
        client_socket.send(str(cpu_count()).encode())
        print("Sent CPU count")
        while free_cpus > 0:
            data = client_socket.recv(1024).decode()
            print("The server sent " + data)
            if "FOUND" not in data:
                msg = data.split("$")[0]
                start = int(data.split("$")[1])
                end = int(data.split("$")[2])

                ends = start + end / cpu_count()
                thread = Thread(target=calculate_password, args=(msg, start, ends))
                free_cpus -= 1
                thread.start()
                threads.append(thread)
                print(f"starting thread number {total_cpu - free_cpus}..")
                start += end / cpu_count()

            print("waits for the threads to end..")
            for thread in threads:
                thread.join()
            client_socket.send(answer.encode())
            print("Sent answer:" + answer)
            client_socket.recv(MAX_PACKET)
            free_cpus = total_cpu
        else:
            print("found the message!\n disconnecting...")
            client_socket.close()
            exit()
    except socket.error as err:
        print(str(err))
        print("disconnecting...")
        client_socket.close()
        exit()
    finally:
        client_socket.close()
        exit()


if __name__ == "__main__":
    main()
