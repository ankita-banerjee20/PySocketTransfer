import os
import socket
import time


def send_file(file_name, host='192.168.29.217', port=9999):
    # Setting up the server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    # Accepting the connection from client
    client_socket, client_add = server_socket.accept()
    print(f'{client_add} is connected!')

    # Opening the file and reading the content
    with open(file_name, 'rb') as file:
        start_time = time.time()
        while True:
            byte_read = file.read(1024) # Reading the file in chunks
            if not byte_read:
                break
            client_socket.sendall(byte_read)
        end_time = time.time()

    print('File Sent Successfully! Time Taken: ', end_time - start_time)

    # Closing the sockets
    client_socket.close()
    server_socket.close()

send_file('data/dog_video.mp4')