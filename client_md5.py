import hashlib
import socket
from os import cpu_count

SERVER_IP = '127.0.0.1'
PORT = 8080
MAX_PACKET = 1024
CHUNK_SIZE = 99999999
ORIGINAL_LEN = 7
NOT_FOUND = "NOT FOUND"


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


def calculate_password(md5_str, start, end):
    while start != end:
        if hashlib.md5(str(start).zfill(ORIGINAL_LEN).encode()).hexdigest() == md5_str:
            return str(start)
        start += 1
    return NOT_FOUND


def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_IP, PORT))
    print("Connected to server")
    client_socket.send(str(cpu_count()).encode())
    print("Sent CPU count")
    MD5_STR = client_socket.recv(MAX_PACKET).decode()
    print("received hash: " + MD5_STR)
    start = int(client_socket.recv(MAX_PACKET).decode())
    print("start: " + str(start))
    end = int(client_socket.recv(MAX_PACKET).decode())
    print("end: " + str(end))
    client_socket.send(calculate_password(MD5_STR, start, end).encode())
    print(calculate_password(MD5_STR, start, end))


if __name__ == "__main__":
    main()
