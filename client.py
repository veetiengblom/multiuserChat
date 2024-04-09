# Import necessary libraries
import socket  # For socket communication
import threading  # For concurrent execution of tasks

IP = '127.0.0.1'
PORT = 3001

nickname = input('Enter your nickname: ')

# Display chat instructions to the user
print(
'''
Welcome to chat

You can use the following commands:

/join *channel name* (Join a channel)
/send *message* (Send message to people in the channel)
/dm *nickname* *message* (Direct message)
/leave (Leave the channel you are connected)
/close (Close the program)
'''
)

# Create a socket object for client-server communication
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try: 
    # Connect to the server
    client_socket.connect((IP, PORT))
except:
    print('Failed to connect to server')
    exit(0)

# Function to handle sending messages to the server
def send_messages():
    while True:
        try:
            text = input('')
            # Prepare message format with user nickname
            message = '{}:{}'.format(nickname, text)
            # Send the message to the server after encoding it to UTF-8
            client_socket.send(message.encode('utf-8'))
            # Check if the user wants to close the connection
            if text == '/close':
                client_socket.close()
                break
        except Exception as e:
            print('disconnecting...')
            break

# Function to handle receiving messages from the server
def receive_messages():
    while True:
        try:
            # Receive messages from the server
            message = client_socket.recv(1024).decode('utf-8')
            # Check if the server requests user identification
            if message == 'USER':
                client_socket.send(nickname.encode('utf-8'))
            else:
                print(message)
        except Exception as e:
            print('disconnecting...')
            break

# Create threads for sending and receiving messages concurrently
threading.Thread(target=receive_messages).start()
threading.Thread(target=send_messages).start()
