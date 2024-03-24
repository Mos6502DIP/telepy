import errno
import socket
import datetime
import time

buffer = 0


def setting(setting: str):

    with open("server_config.txt") as fp:
        lines = fp.readlines()
        for line in lines:
            if line.strip()[0] != "#":
                setting_line = line.strip().split("=")
                if setting_line[0] == setting:
                    return setting_line[1]


def test():
    print(f"You are using telepy!")


def log(filename, text):
    print(text)
    with open(filename, 'a') as file:
        file.write(text + '\n')


def setup():

    Sct = socket.socket()  # creating the socket
    ports = int(setting("port"))
    Sct.bind(("", int(ports)))  # Bind port
    Sct.listen(int(setting("listen")))  # listens for clients
    print(f'Tele py server started on port:{ports} and listening for {setting("listen")} Clients!')
    return Sct


def setup_log(log_file):

    Sct = socket.socket()  # creating the socket
    ports = setting("port")
    Sct.bind(("", int(ports)))  # Bind port
    Sct.listen(int(setting("listen")))  # listens for clients
    log(log_file, f'Tele py server started on port:{ports} and listening for {setting("listen")} Clients!')
    return Sct


def printt(string, client):
    try:
        time.sleep(buffer)
        client.send(bytes(f"0{string}", "utf-8"))

        acknowledgment = client.recv(1024).decode()
        if acknowledgment != "ACK":
            print("Error: Client did not acknowledge the message.")

    except socket.error as e:
        if e.errno != 10038 and e.errno != 10054:
            print(f"Socket error: {e}")


def inputt(string, client):
    try:
        time.sleep(buffer)
        client.send(bytes(f"1{string}", "utf-8"))

        acknowledgment = client.recv(1024).decode()
        if acknowledgment != "ACK":
            print("Error: Client did not acknowledge the message.")

        return client.recv(1024).decode()
    except socket.error as e:
        if e.errno != 10038 and e.errno != 10054:
            print(f"Socket error: {e}")

        return None


def closet(log_file, string, client, add):
    try:
        time.sleep(buffer)
        client.send(bytes(f"2{string}", "utf-8"))

        acknowledgment = client.recv(1024).decode()
        if acknowledgment != "ACK":
            print("Error: Client did not acknowledge the message.")

        client.close()
        log(log_file, f"{add} has disconnected from the server at {datetime.datetime.now()}")
    except socket.error as e:
        if e.errno != 10038 and e.errno != 10054:
            print(f"Socket error: {e}")


def cls(client):
    try:
        time.sleep(buffer)
        client.send(bytes(f"3", "utf-8"))

        acknowledgment = client.recv(1024).decode()
        if acknowledgment != "ACK":
            print("Error: Client did not acknowledge the message.")

    except socket.error as e:

        if e.errno != 10038 and e.errno != 10054:
            print(f"Socket error: {e}")


def blankline(client):
    try:
        time.sleep(buffer)
        client.send(bytes(f"4", "utf-8"))

        acknowledgment = client.recv(1024).decode()
        if acknowledgment != "ACK":
            print("Error: Client did not acknowledge the message.")

    except socket.error as e:
        if e.errno != 10038 and e.errno != 10054:
            print(f"Socket error: {e}")


def password(string, client):
    try:
        time.sleep(buffer)
        client.send(bytes(f"5{string}", "utf-8"))

        acknowledgment = client.recv(1024).decode()
        if acknowledgment != "ACK":
            print("Error: Client did not acknowledge the message.")

        return client.recv(1024).decode()
    except socket.error as e:
        if e.errno != 10038 and e.errno != 10054:
            print(f"Socket error: {e}")

        return None


def client_version(client):
    try:
        time.sleep(buffer)
        client.send(bytes(f"6ver", "utf-8"))

        acknowledgment = client.recv(1024).decode()
        if acknowledgment != "ACK":
            print("Error: Client did not acknowledge the message.")

        return client.recv(1024).decode()
    except socket.error as e:
        if e.errno != 10038 and e.errno != 10054:
            print(f"Socket error: {e}")

        return None


def system_command(string, client):
    try:
        time.sleep(buffer)
        client.send(bytes(f"7{string}", "utf-8"))

        acknowledgment = client.recv(1024).decode()
        if acknowledgment != "ACK":
            print("Error: Client did not acknowledge the message.")

    except socket.error as e:
        if e.errno != 10038 and e.errno != 10054:
            print(f"Socket error: {e}")


def hidden_input(string, client):
    try:
        time.sleep(buffer)
        client.send(bytes(f"8{string}", "utf-8"))

        acknowledgment = client.recv(1024).decode()
        if acknowledgment != "ACK":
            print("Error: Client did not acknowledge the message.")

        return client.recv(1024).decode()
    except socket.error as e:
        if e.errno != 10038 and e.errno != 10054:
            print(f"Socket error: {e}")

        return None
