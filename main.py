from cryptography.fernet import Fernet
import base64
import hashlib
import socket
import threading
from rich import print
from datetime import datetime
import platform
import subprocess

os_info = platform.system()
now = datetime.now()
current_datetime = now.strftime("%Y-%m-%d %H:%M:%S")

def generate_key(user_input):
    key = hashlib.sha256(user_input.encode()).digest()
    return base64.urlsafe_b64encode(key)

def encrypt_message(message, key):
    fernet = Fernet(key)
    encrypted = fernet.encrypt(message.encode())
    return encrypted

def decrypt_message(encrypted_message, key):
    fernet = Fernet(key)
    decrypted = fernet.decrypt(encrypted_message).decode()
    return decrypted

main_menu = f'''
Твой хост: {socket.gethostname()}

1. Подключение к компьютеру
2. Сервер
3. Настройки
'''

print(main_menu)

try:
    number = int(input("--> "))

    def receive_messages(client_socket):
        while True:
            try:
                data = client_socket.recv(1024)
                if not data:
                    break
                print(f"Получено от сервера: [blue]{data.decode()}[/blue]")
            except:
                print("Ошибка при получении сообщения.")
                break

    if number == 1:
        host = input("Введи хост --> ")
        port = int(input("Введи порт --> "))
        user_input = input("Ключ для шифрования -->")
        key = generate_key(user_input)

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        print()
        print("Подключение к серверу установлено")
        print()
        thread = threading.Thread(target=receive_messages, args=(client_socket,))
        thread.start()

        while True:
            message = input()
            encrypted_message = encrypt_message(message, key)
            client_socket.sendall(encrypted_message)

    if number == 2:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('localhost', 12345))
        server_socket.listen(1)
        print("Ожидание подключения к серверу...")
        client_socket, addr = server_socket.accept()
        print()
        print(f"Подключение установлено к {addr}")
        print()

        def receive_messages_server(client_socket):
            while True:
                try:
                    data = client_socket.recv(1024)
                    with open('message/message.txt', 'r+') as file:
                        file.write(f'{current_datetime}: {data.decode()}')
                except:
                    print("[red]Ошибка при получении сообщения. [/red]")
                    break

        thread = threading.Thread(target=receive_messages_server, args=(client_socket,))
        thread.start()

        while True:
            message = input()
            client_socket.sendall(message.encode())

    if number == 3:
        print("1. Задать пароль для шифрования")

except ConnectionRefusedError:
    print("Connection refused")

except OSError:
    print("Подождите несколько секунд чтобы запустить сервер")

except KeyboardInterrupt:
    print("\n\nBye Bye!\n")
    
