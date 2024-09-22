# Importing necessary libraries
import socket
import threading

host = '192.168.29.217'
port = 9999
client_limit = 5
active_clients = []  # List to keep track of all connected clients


# Function to listen to messages from client
def listen_to_msg(client_socket, username):
    while True:
        try:
            message = client_socket.recv(1024).decode() # Receives message from client
            if message != '':
                decorated_message = username + '-' + message
                send_msg_to_others(decorated_message, client_socket)  
            else:
                print(f'The message sent from {username} is empty')
                break
        except:
            print(f'{username} has disconnected')
            active_clients.remove((username, client_socket))
            prompt_message = 'SERVER-' + f'{username} has left the chat.'
            send_msg_to_all(prompt_message)
            break




# Function to send message to single client
def send_msg_to_client(client_socket, message):
    try:
        client_socket.sendall(message.encode())
    except:
        print(f'Error sending message to {client_socket}')



# Function to send message to all clients except the sender
def send_msg_to_others(message, sender_socket):
    for user in active_clients:
        if user[1] != sender_socket:  
            send_msg_to_client(user[1], message)


# Function to send message to all the clients
def send_msg_to_all(message):
    # Send message to all clients 
    for user in active_clients:
        send_msg_to_client(user[1], message)


# Function to handle client
def client_handler(client_socket):
    while True:
        try:
            username = client_socket.recv(1024).decode() # Receives username from client
            if username != '':
                active_clients.append((username, client_socket))
                prompt_message = 'SERVER-' + f'{username} joined the chat!'
                send_msg_to_all(prompt_message)
                break
            else:
                print('Username is empty!')
                client_socket.close()
        except:
            print('Error receiving username')
            client_socket.close()
            exit(0)

    # Starting a new thread to listen for incoming messages from this client
    threading.Thread(target=listen_to_msg, args=(client_socket, username)).start()


# Main function
def main():
    # Setting up the server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((host, port))
        print(f'Running the server on {host} {port}')
    except:
        print(f'Unable to bind the server on {host} {port}')
        exit(0)

    # Setting the server limit
    server.listen(client_limit)
    print(f'Server is listening up to {client_limit} clients')

    # Listening to all client connections
    while True:
        client_socket, client_add = server.accept()
        print(f'Successfully Connected to client {client_add[0]} {client_add[1]}')

        # Starting a new thread to handle the client
        threading.Thread(target=client_handler, args=(client_socket,)).start()



if __name__ == '__main__':
    main()

