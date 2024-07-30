from cryptography.fernet import Fernet
import socket
import threading

# check your host
try:
    with open('host.txt', 'r+') as file:
        host = file.readlines()
        host = host[0]
except:
    if host == []:
        host = input("Your HOST --> ")
        with open('host.txt', 'r+') as file:
            file.write(host)

try:
    with open('port.txt', 'r+') as file:
        port = file.readlines()
        port = port[0]
except:
    if port == []:
        port = input("Your PORT --> ")
        with open('port.txt', 'r+') as file:
            file.write(port)

print(f"Твой хост: {socket.gethostname()}")

print("1. Подключение к компьютеру")
print("2. Сервер")
print("3. Настройки")

number = int(input("--> "))

def receive_messages(client_socket):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            print(f"Получено от сервера: {data.decode()}")
        except:
            print("Ошибка при получении сообщения.")
            break

if number == 1:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))

    thread = threading.Thread(target=receive_messages, args=(client_socket,))
    thread.start()

    while True:
        message = input()
        client_socket.sendall(message.encode())

if number == 2:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(1)
    print("[log] Ожидание подключения к серверу...")
    client_socket, addr = server_socket.accept()
    print(f"[log] Подключено к {addr}")

    def receive_messages_server(client_socket):
        while True:
            try:
                data = client_socket.recv(1024)
                if not data:
                    break
                print(f"{addr}: {data.decode()}")
            except:
                print("Ошибка при получении сообщения.")
                break

    thread = threading.Thread(target=receive_messages_server, args=(client_socket,))
    thread.start()

    while True:
        message = input("--> ")
        client_socket.sendall(message.encode())
if number == 3:
    pass