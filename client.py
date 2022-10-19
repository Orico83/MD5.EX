import socket

IP = '127.0.0.1'
PORT = 8080

my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_socket.connect((IP, PORT))