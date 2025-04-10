import socket
import json
import sys


sct = socket.socket()

sct.connect(("127.0.0.1", 1969))

server_rev = sct.recv(1024).decode()

print(server_rev)

sct.send(bytes(f"funny", "utf-8"))

while True:
    data= sct.recv(2323).decode()
    print(data)
    list = json.loads(data)
    print(f"Received {sys.getsizeof(list)} bytes now sending confirmation.")
    sct.send(bytes(json.dumps(list), "utf-8"))