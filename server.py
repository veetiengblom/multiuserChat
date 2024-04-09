#Used help from this tutorial: https://www.youtube.com/watch?v=nmzzeAvQHp8&ab_channel=BekBrace
# Import necessary libraries
import socket  # For socket communication
import threading  # For concurrent execution of tasks

HOST = '127.0.0.1'
PORT = 3001

clients = [] 
nicknames = []  
channels = {} 

# Function to remove a client from a channel
def remove_from_channel(client, channel_name, nickname):
    for clients in channels.values():
        if client in clients:   
            clients.remove(client)
            send_to_channel(client, channel_name, f'{nickname} left channel')
            client.send(f'You left channel: {channel_name}'.encode('utf-8'))
            print(f'{nickname} left channel: {channel_name}')
            break
    return


# Function to add a client to a channel
def join_channel(client, channel_name, nickname):
    if channel_name in channels:
        #Add client to a channel
        channels[channel_name].append(client)
        
        send_to_channel(client, channel_name, f'{nickname} joined channel')
        print(f'{nickname} joined channel: {channel_name}')
    else:
        # Create a new channel and add the client
        channels[channel_name] = [client]
       
        send_to_channel(client, channel_name, f'{nickname} joined channel')
        print(f'{nickname} joined channel: {channel_name}')
    return


# Function to send a message to a channel
def send_to_channel(client, channel_name, message):
    if channel_name is None:
        client.send(('Join channel to send messages /join *channel name*').encode('utf-8'))
        return 
    for client in channels[channel_name]:
        print('client', client)
        client.send(message.encode('utf-8'))
    return 


# Function to send a direct message to a user
def dm_to_user(message, receiver, client):
    if receiver is None:
        client.send('No user found'.encode('utf-8'))
        return
    receiver.send(message.encode('utf-8'))
    return


# Function to find a user by nickname
def find_user(receiver):
    for user in nicknames:
        if user[0] == receiver:
            return user[1]
    return


# Function to find the channel associated with a client
def find_channel(client):
    for channel, clients in channels.items():
        if client in clients:
            print('channel', channel)
            return channel
    return None


# Function to handle client messages
def handler(client):
    while True:
        try: 
            message = client.recv(1024).decode('utf-8')
            nickname, text = message.split(':')
            text = text.strip()
            if text == '/close':
                send_to_channel(client, find_channel(client), f'{nickname} left channel')
                print(f'{nickname} disconnected')
                nicknames.remove((nickname, client))
                client.close()
                break
        except Exception as e:
            nicknames.remove((nickname, client))
            print(nicknames)
            send_to_channel(client, find_channel(client), f'{nickname} left channel')
            break

        # Check for special commands
        if text.startswith('/join '):
            channel_name = message.split(' ', 1)[1]
            remove_from_channel(client, channel_name, nickname)
            join_channel(client, channel_name, nickname)
        elif text.startswith('/send '):
            message = message.split(' ', 1)[1]
            send_to_channel(client, find_channel(client), message)
        elif text.startswith('/dm '):
            receiver, text = message.split(' ', 2)[1:3]
            message = (f'Direct message: {text} \nfrom: {nickname}')
            dm_to_user(message, find_user(receiver), client)
        elif text.startswith('/leave'):
            remove_from_channel(client, channel_name, nickname)


# Function to accept incoming connections
def main():
    # Create a socket object for server-client communication
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the host and port
    server_socket.bind((HOST, PORT))

    server_socket.listen()

    
    while True:
        client, address = server_socket.accept()
        print(f'{str(address)} connected')
        client.send('alias'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append((nickname, client))
        clients.append(client)
        client.send('Connected to server'.encode('utf-8'))
        # Start a new thread to handle client messages
        threading.Thread(target=handler, args=(client,)).start()

print(f'Server running at: {HOST}:{PORT}')
if __name__ == '__main__':
    main()
