import hashlib
import socket
from os import cpu_count
from threading import Thread

SERVER_IP = '127.0.0.1'
PORT = 8080
MAX_PACKET = 1024
CHUNK_SIZE = 2000000
ORIGINAL_LEN = 7
answer = "NOT FOUND"
free_cpus = cpu_count()
total_cpu = cpu_count()
threads = []
starts = 0
mid = 0
ends = 0

"""def divide_md5(md5_str, start, end):
    found = False
    while not found:
        check_pass = calculate_password(start, end, md5_str)
        if check_pass != NOT_FOUND:
            found = True
        else:
            start = end
            end += CHUNK_SIZE / cpu_count()
    return check_pass"""


def give_range(start, end):
    """
    gives range to the client threads.
    :param start: int
    :param end: int
    :return: start and mid
    """
    global starts
    global ends
    starts = start
    ends = starts + CHUNK_SIZE
    return starts, ends


def calculate_password(md5_str, strt, end):
    global answer
    while strt != end:
        if hashlib.md5(str(strt).zfill(ORIGINAL_LEN).encode()).hexdigest() == md5_str:
            answer = str(strt)
        strt += 1
    print(answer)


def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_IP, PORT))
    print("Connected to server")
    try:
        while True:
            client_socket.send(str(cpu_count()).encode())
            print("Sent CPU count")
            data = client_socket.recv(1024).decode()
            print("The server sent " + data)
            if "FOUND" not in data:
                global free_cpus
                global total_cpu
                global starts
                global mid
                global ends
                global plus
                while True:
                    msg = data.split("$")[0]
                    start = int(data.split("$")[1])
                    end = int(data.split("$")[2])
                    while free_cpus > 0:
                        lis = give_range(start, end)
                        st = lis[0]
                        en = lis[1]
                        thread = Thread(target=calculate_password, args=(msg, st, en))
                        free_cpus -= 1
                        thread.start()
                        threads.append(thread)
                        print(f"starting thread number {total_cpu - free_cpus}..")
                        client_socket.send(answer.encode())
                        starts = 0
                        mid = 0
                        ends = 0
                        plus = 1 + starts
                        break
                    if free_cpus == 0:
                        print("waits for the threads to end..")
                        for thread in threads:
                            thread.join()
                        free_cpus = total_cpu
                    break
                break
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
