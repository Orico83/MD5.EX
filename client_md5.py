import hashlib
import socket
import multiprocessing
from os import cpu_count

SERVER_IP = '127.0.0.1'
PORT = 8080
MAX_PACKET = 1024
CHUNK_SIZE = 99999999
ORIGINAL_LEN = 7
NOT_FOUND = "NOT FOUND"


def divide_md5(md5_str, start):
    end = start + CHUNK_SIZE / int(cpu_count())
    found = False
    while not found:
        check_pass = calculate_password(start, end, md5_str)
        if check_pass != NOT_FOUND:
            found = True
        else:
            start = end
            end += CHUNK_SIZE / cpu_count()
    return check_pass


def calculate_password(start, end, md5_str):
    while start != end:
        if hashlib.md5(str(start).zfill(ORIGINAL_LEN).encode()).hexdigest() == md5_str:
            return str(start)
        start += 1
    return NOT_FOUND


def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_IP, PORT))
    client_socket.send(str(cpu_count()).encode())
    MD5_STR = client_socket.recv(MAX_PACKET).decode()
    start = int(client_socket.recv(MAX_PACKET).decode())
    end = int(client_socket.recv(MAX_PACKET).decode())
    print(MD5_STR)
    client_socket.send(divide_md5(MD5_STR, start).encode())
    print(divide_md5(MD5_STR, start))


if __name__ == "__main__":
    main()
