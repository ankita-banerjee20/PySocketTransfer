# Importing necessary libraries
import socket
import threading

host = '192.168.29.217'
port = 9999

# Function to receive message from the server
def listen_to_msg_from_server(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message != '':
                content_list = message.split('-')
                if len(content_list) == 2:
                    username = content_list[0]
                    content = content_list[1]
                    print(f'[{username}] {content}')
                else:
                    print('Received improperly formatted message')
            else:
                print('Message is empty!')
        except:
            print('Connection lost to the server')
            client_socket.close()
            break




# Function to take user message and send it to server
def send_msg_to_server(client_socket):
    while True:
        try:
            message = input()
            if message != '':
                client_socket.sendall(message.encode())
            else:
                print('Message is empty!')
        except:
            print('Failed to send message')
            client_socket.close()
            break



# Function to communicate with the server
def communicate_with_server(client_socket):
    # Sending username to the server
    username = input('Enter Username: ')
    if username != '':
        client_socket.sendall(username.encode())
    else:
        print('Username is Empty!')
        client_socket.close()
        exit(0)

    # Starting a new thread to listen for messages from the server
    threading.Thread(target=listen_to_msg_from_server, args=(client_socket,)).start()

    # Sending message to the server
    send_msg_to_server(client_socket)


# Main function
def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client_socket.connect((host, port))
        print('Successfully Connected to Server!')
    except:
        print('Unable to Connect to Server!')
        exit(0)

    communicate_with_server(client_socket)



if __name__ == '__main__':
    main()