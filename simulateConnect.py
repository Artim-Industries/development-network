import socket
import sys
import time
import os
import json
from cryptography.fernet import Fernet

host = "127.0.0.1"
port = 17787

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
client, address = server.accept()
print("Connected with " + address[0])
client.send('connected'.encode('ascii'))
while True:
    message = client.recv(1024).decode('ascii')

    if message == "getNetwork":
        client.send('networkNextMessage'.encode('ascii'))
        size = str(os.path.getsize(r'network\network.json'))
        client.send(size.encode('ascii'))
        
        with open(r"network\network.json") as f:
            data = json.load(f)
        
        dataR = str(data)
        key = Fernet.generate_key()
        fernet = Fernet(key)
        encrypted = fernet.encrypt(dataR.encode())
        toSend = key + encrypted
        client.send(toSend)
    print(message)