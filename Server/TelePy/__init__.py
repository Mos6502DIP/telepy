import socket
import datetime
import time
import json
import sys
import threading


buffer = 0

settings = {}

active_terminal_clients = set()
active_terminal_clients_lock = threading.Lock()

def settings():
    global settings
    with open('config.txt', "r") as f:
        settings = json.load(f)


def test():
    print(f"You are using telepy!")


def log(filename, text):
    print(text)
    with open(filename, 'a') as file:
        file.write(text + '\n')


def setup():
    global settings
    Sct = socket.socket()  # creating the socket
    ports = settings["port"]
    Sct.bind(("", int(ports)))  # Bind port
    Sct.listen(settings["listen"])  # listens for clients
    print(f'Tele py server started on port:{ports} and listening for {settings["listen"]} Clients!')
    return Sct


def setup_log(log_file):
    global settings
    Sct = socket.socket()  # creating the socket
    ports = settings["port"]
    Sct.bind(("", int(ports)))  # Bind port
    Sct.listen(settings["listen"])  # listens for clients
    log(log_file, f'Tele py server started on port:{ports} and listening for {settings["listen"]} Clients!')
    return Sct

def tele_net():
    global settings

def handle_connection_wrapper(client_socket, client_address):
    try:
        # Your actual connection handling logic here
        print(f"Handling client {client_address}")
        
        # Simulating some handling logic (e.g., waiting for data, interacting with the client)
        data = client_socket.recv(1024).decode().strip()
        if data:
            print(f"Received data from {client_address}: {data}")
        else:
            print(f"No data received from {client_address}")

    finally:
        # When the connection ends, remove the thread from active clients
        with active_terminal_clients_lock:
            active_terminal_clients.discard(threading.current_thread())
        print(f"Client {client_address} disconnected. {len(active_terminal_clients)} terminal clients online.")
        client_socket.close()

def start(client_side, log=False, log_file=False):
    # Socket setup
    if log:
        if log_file:
            sct = setup_log(log_file)
        else:
            exit(1)
    else:
        sct = setup(log_file)

    # Threading cleanup
    cleanup_thread = threading.Thread(target=clean_dead_threads, daemon=True)
    cleanup_thread.start()
    
    # Main server script
    while True:
        client_socket, client_address = sct.accept()
        print(f"Connection from {client_address}")
        client_socket.settimeout(10)

        try:
            # Receive connection type (like 'terminal') from the client
            connection_type = client_socket.recv(1024).decode().strip()
        except socket.timeout:
            print(f"Timeout from {client_address}")
            client_socket.close()
            continue

        if connection_type == 'terminal':
           
            client_thread = threading.Thread(
                target=handle_connection_wrapper,
                args=(client_side, client_socket, client_address),
                name=f"TerminalClient-{client_address}"
            )
            client_thread.start()

            with active_terminal_clients_lock:
                active_terminal_clients.add(client_thread)

            print(f"{len(active_terminal_clients)} terminal clients online.")
        else:
            print(f"Unknown connection type '{connection_type}' from {client_address}")
            client_socket.close()


class Client:

    def __init__(self, client_id, client_ip):
        self.client = client_id
        self.client_ip = client_ip

    def print(self, string):
        try:
            time.sleep(buffer)
            self.client.send(bytes(f"0|{string}", "utf-8"))

            acknowledgment = self.client.recv(1024).decode()
            if acknowledgment != "ACK":
                print("Error: Client did not acknowledge the message.")


        except socket.error as e:
            if e.errno != 10038 and e.errno != 10054:
                print(f"Socket error: {e}")


    def input(self, string):
        try:
            time.sleep(buffer)
            self.client.send(bytes(f"1|{string}", "utf-8"))

            acknowledgment = self.client.recv(1024).decode()
            if acknowledgment != "ACK":
                print("Error: Client did not acknowledge the message.")

            return self.client.recv(1024).decode()
        except socket.error as e:
            if e.errno != 10038 and e.errno != 10054:
                print(f"Socket error: {e}")

            return None


    def closet_log(self, log_file, string):
        try:
            time.sleep(buffer)
            self.client.send(bytes(f"2|{string}", "utf-8"))

            acknowledgment = self.client.recv(1024).decode()
            if acknowledgment != "ACK":
                print("Error: Client did not acknowledge the message.")

            self.client.close()
            log(log_file, f"{self.client_ip} has disconnected from the server at {datetime.datetime.now()}")
        except socket.error as e:
            if e.errno != 10038 and e.errno != 10054:
                print(f"Socket error: {e}")


    def cls(self):
        try:
            time.sleep(buffer)
            self.client.send(bytes(f"3|", "utf-8"))

            acknowledgment = self.client.recv(1024).decode()
            if acknowledgment != "ACK":
                print("Error: Client did not acknowledge the message.")

        except socket.error as e:

            if e.errno != 10038 and e.errno != 10054:
                print(f"Socket error: {e}")


    def blankline(self):
        try:
            time.sleep(buffer)
            self.client.send(bytes(f"4|", "utf-8"))

            acknowledgment = self.client.recv(1024).decode()
            if acknowledgment != "ACK":
                print("Error: Client did not acknowledge the message.")

        except socket.error as e:
            if e.errno != 10038 and e.errno != 10054:
                print(f"Socket error: {e}")


    def password(self, string):
        try:
            time.sleep(buffer)
            self.client.send(bytes(f"5|{string}", "utf-8"))

            acknowledgment = self.client.recv(1024).decode()
            if acknowledgment != "ACK":
                print("Error: Client did not acknowledge the message.")

            return self.client.recv(1024).decode()
        except socket.error as e:
            if e.errno != 10038 and e.errno != 10054:
                print(f"Socket error: {e}")

            return None


    def client_version(self):
        try:
            time.sleep(buffer)
            self.client.send(bytes(f"6|", "utf-8"))

            acknowledgment = self.client.recv(1024).decode()
            if acknowledgment != "ACK":
                print("Error: Client did not acknowledge the message.")

            device = self.client.recv(1024).decode()
            return device
        except socket.error as e:
            if e.errno != 10038 and e.errno != 10054:
                print(f"Socket error: {e}")

            return None


    def weather(self):
        try:
            time.sleep(buffer)
            self.client.send(bytes(f"7|dummy", "utf-8"))

            acknowledgment = self.client.recv(1024).decode()
            if acknowledgment != "ACK":
                print("Error: Client did not acknowledge the message.")

        except socket.error as e:
            if e.errno != 10038 and e.errno != 10054:
                print(f"Socket error: {e}")


    def hidden_input(self, string):
        try:
            time.sleep(buffer)
            self.client.send(bytes(f"8|{string}", "utf-8"))

            acknowledgment = self.client.recv(1024).decode()
            if acknowledgment != "ACK":
                print("Error: Client did not acknowledge the message.")

            return self.client.recv(1024).decode()
        except socket.error as e:
            if e.errno != 10038 and e.errno != 10054:
                print(f"Socket error: {e}")

            return None


    def printc(self, string, color):
        colours = ["black", "red", "green", "yellow", "blue", "magenta", "cyan",
                   "light_red", "light_green", "light_yellow",
                   "light_blue", "light_magenta", "light_cyan", "white"]  # compatible colours

        try:
            time.sleep(buffer)
            if len(color) == 1:
                color.append("black")
            if color[0] in colours:
                if color[1] in colours:
                    self.client.send(bytes(f"9|{json.dumps(color)}|{string}", "utf-8"))

            else:
                print("Error: Invalid colour")
                self.client.send(bytes(f"9|{['white']}|{string}", "utf-8"))


            acknowledgment = self.client.recv(1024).decode()
            if acknowledgment != "ACK":
                print("Error: Client did not acknowledge the message.")

        except socket.error as e:
            if e.errno != 10038 and e.errno != 10054:
                print(f"Socket error: {e}")


    def print2d(self, array):


        try:
            time.sleep(buffer)

            self.client.send(bytes(f"10|{json.dumps(array)}", "utf-8"))

            acknowledgment = self.client.recv(1024).decode()
            if acknowledgment != "ACK":
                print("Error: Client did not acknowledge the message.")

        except socket.error as e:
            if e.errno != 10038 and e.errno != 10054:
                print(f"Socket error: {e}")


    def print2dc(self, array):
        try:
            time.sleep(buffer)
            self.client.send(bytes(f"11|{json.dumps(array)}", "utf-8"))
            acknowledgment = self.client.recv(1024).decode()
            if acknowledgment != "ACK":
                print("Error: Client did not acknowledge the message.")

        except socket.error as e:
            if e.errno != 10038 and e.errno != 10054:
                print(f"Socket error: {e}")


    def set_mode(self, mode):
        try:
            time.sleep(buffer)
            self.client.send(bytes(f"12|{mode}", "utf-8"))
            acknowledgment = self.client.recv(1024).decode()
            if acknowledgment != "ACK":
                print("Error: Client did not acknowledge the message.")

        except socket.error as e:
            if e.errno != 10038 and e.errno != 10054:
                print(f"Socket error: {e}")


    def get_key_state(self, key):
        try:
            time.sleep(buffer)
            self.client.send(bytes(f"13|{key}", "utf-8"))



            acknowledgment = self.client.recv(1024).decode()

            key = self.client.recv(1024).decode()
            if acknowledgment != "ACK":
                print("Error: Client did not acknowledge the message.")

            return key
        except socket.error as e:
            if e.errno != 10038 and e.errno != 10054:
                print(f"Socket error: {e}")

            return None

    def device(self):
        try:
            time.sleep(buffer)
            self.client.send(bytes(f"14|", "utf-8"))

            acknowledgment = self.client.recv(1024).decode()
            if acknowledgment != "ACK":
                print("Error: Client did not acknowledge the message.")

            device = self.client.recv(1024).decode()
            return device
        except socket.error as e:
            if e.errno != 10038 and e.errno != 10054:
                print(f"Socket error: {e}")

            return None
        
    def switch(self, string):
        try:
            time.sleep(buffer)
            self.client.send(bytes(f"15|{string}", "utf-8"))

            acknowledgment = self.client.recv(1024).decode()
            if acknowledgment != "ACK":
                print("Error: Client did not acknowledge the message.")

            status = self.client.recv(1024).decode()

            if status == 'switch':
                self.client.close()
                print(f"{self.client_ip} has switched from the server at {datetime.datetime.now()} to {string}")
                return True
            else:
                return False
        except socket.error as e:
            if e.errno != 10038 and e.errno != 10054:
                print(f"Socket error: {e}")

            return None

    def closet(self, string):
        try:
            time.sleep(buffer)
            self.client.send(bytes(f"15|{string}", "utf-8"))

            acknowledgment = self.client.recv(1024).decode()
            if acknowledgment != "ACK":
                print("Error: Client did not acknowledge the message.")

            self.client.close()
            print(f"{self.client_ip} has disconnected from the server at {datetime.datetime.now()}")
        except socket.error as e:
            if e.errno != 10038 and e.errno != 10054:
                print(f"Socket error: {e}")





