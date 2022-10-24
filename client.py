import hashlib
import socket
import multiprocessing


IP = '127.0.0.1'
PORT = 8080
MD5_STR = "81dc9bdb52d04dc20036dbd8313ed055"
"""my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_socket.connect((IP, PORT))"""



def divide_md5(md5_str):
    start = 0
    md5_len = len(md5_str)
    cpu_count = multiprocessing.cpu_count()
    end = 10000 / cpu_count
    found = False
    while not found:
        new_pass = calculate_password(start, end, md5_str)
        if new_pass != "NOT FOUND":
            found = True
        else:
            start = end + 1
            end += md5_len / cpu_count
    return new_pass


def calculate_password(start, end, md5_str):
    while start != end:
        if hashlib.md5(str(start).encode()).hexdigest() == md5_str:
            return str(start)
        start += 1
    return "NOT FOUND"


def main():
    print(divide_md5(MD5_STR))


if __name__ == "__main__":
    main()