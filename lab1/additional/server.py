import threading
import socket

host = '127.0.0.1'
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} вийшов з чату'.encode('utf-8'))
            nicknames.remove(nickname)
            break

def receive():
    while True:
        client, address = server.accept()
        print(f'Пов\'язано з {str(address)}')

        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)

        print(f'Нік клієнта: {nickname}!')
        broadcast(f'{nickname} приєднався до чату!'.encode('utf-8'))
        client.send('Підключення до сервера!'.encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Сервер слухає...")
receive()
