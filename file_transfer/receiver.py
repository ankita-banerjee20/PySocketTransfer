import socket
import time


def receive_file(save_path, host='192.168.29.217', port=9999):
    # Setting up the client server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connecting to the server
    try:
        client_socket.connect((host, port))
        print('Connected Successfully!')
    except:
        print('Unable to Connect!')
        exit(0)

    # Opening the file and writing the content
    with open(save_path, 'wb') as file:
        start_time = time.time()
        while True:
            byte_read = client_socket.recv(1024) # Receiving the data in chunks
            if not byte_read:
                break
            file.write(byte_read)
        end_time = time.time()

    print('File Received Successfully! Time Taken: ', end_time - start_time)

    # Closing the socket
    client_socket.close()

receive_file('rec/dog_video.mp4')

