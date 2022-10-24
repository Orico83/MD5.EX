import hashlib
import socket

IP = '127.0.0.1'
PORT = 8080
MD5_STR = "81dc9bdb52d04dc20036dbd8313ed055"
"""my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_socket.connect((IP, PORT))"""


def calculate_range(start, end, md5_str):
    while start != end:
        if hashlib.md5(str(start).encode()).hexdigest() == md5_str:
            return str(start)
        start += 1
    return "NOT FOUND"


def main():
    print(calculate_range(0, 2000, MD5_STR))


if __name__ == "__main__":
    main()