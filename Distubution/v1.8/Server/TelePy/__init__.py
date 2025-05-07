import socket
import datetime
import time
import json
import time
import threading


buffer = 0

settings = {}

active_terminal_clients = set()
active_terminal_clients_lock = threading.Lock()

start_time = None

def load_config():
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

def start_uptime():
    global start_time
    start_time = time.time()

def get_uptime():
    global start_time
    if start_time is None:
        return "Uptime not started."
    elapsed_time = time.time() - start_time
    hours, remainder = divmod(int(elapsed_time), 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours}h {minutes}m {seconds}s"

def get_info(server_ip):
    server = server_ip.split(':')
    port = 1998
    if len(server) == 2:

        server_ip = server[0]

        port = int(server[1])

    Sct = socket.socket()
    Sct.connect((server_ip, port))
    Sct.send(bytes('json', "utf-8"))
    server_json = Sct.recv(6000).decode()
    Sct.close()
    return json.loads(server_json)
        
def ping(server_ip):
    server = server_ip.split(':')
    port = 1998
    if len(server) == 2:

        server_ip = server[0]

        port = int(server[1])

    try:
        Sct = socket.socket()
        Sct.settimeout(5)  # Optional: timeout after a few seconds

        start_time = time.time()
        Sct.connect((server_ip, port))
        
        Sct.send(b'ping')  # Send "ping"
        
        response = Sct.recv(1024).decode()
        end_time = time.time()

        Sct.close()

        if response.strip().lower() == "pong":
            ping_ms = (end_time - start_time) * 1000  # Convert to milliseconds
            return ping_ms
        else:
            return None

    except (socket.timeout, socket.error) as e:
        return None

def handle_client_connection_wrapper(client_side, client):
    try:
        print(f"Handling client {client.client_ip}")
        
        client_side(client)

    finally:
        
        with active_terminal_clients_lock:
            active_terminal_clients.discard(threading.current_thread())
        print(f"Client {client.client_ip} disconnected. {len(active_terminal_clients)} terminal clients online.")
        client.client.close()


def handle_ping_connection_wrapper(client_socket):
    try:
        client_socket.send(bytes("pong", "utf-8"))

    finally:

        client_socket.close()


def handle_json_connection_wrapper(client_socket):
    try:
        server_info = {
            'name':settings['server_name'],
            'description':settings['description'],
            'icon':settings['icon'],
            'uptime':get_uptime(),
            'online':len(active_terminal_clients)
        }
            
        client_socket.send(bytes(json.dumps(server_info), "utf-8"))

    finally:

        client_socket.close()



def start(client_side, log_file=False):
    # Loading config
    load_config()

    # Uptime
    start_uptime()

    # Socket setup
    if log_file:
        sct = setup_log(log_file)
    else:
        sct = setup()
    
        
    
    # Main server script
    while True:
        client_socket, client_address = sct.accept()
        print(f"Connection from {client_address}")
        client_socket.settimeout(5)

        try:
            # Receive connection type (like 'terminal') from the client
            connection_type = client_socket.recv(1024).decode().strip()
        except socket.timeout:
            print(f"Timeout from {client_address}")
            client_socket.close()
            continue

        if connection_type == 'terminal':
            client_obj = Client(client_socket, client_address)

            client_thread = threading.Thread(
                target=handle_client_connection_wrapper,
                args=(client_side, client_obj),
                name=f"TerminalClient-{client_address}"
            )
            client_thread.start()

            with active_terminal_clients_lock:
                active_terminal_clients.add(client_thread)

            print(f"{len(active_terminal_clients)} terminal clients online.")

        elif connection_type == 'ping':

            ping_thread = threading.Thread(
                target=handle_ping_connection_wrapper,
                args=(client_socket, ),
                name=f"Ping-{client_address}"
            )
            ping_thread.start()

        elif connection_type == 'json':

            ping_thread = threading.Thread(
                target=handle_json_connection_wrapper,
                args=(client_socket, ),
                name=f"Json-{client_address}"
            )
            ping_thread.start()

        else:
            print(f"Unknown connection type '{connection_type}' from {client_address}")
            client_socket.close()


class Client:

    def __init__(self, client_id, client_ip):
        self.client = client_id
        self.client_ip = client_ip

    def print(self, string):
        try:
            string = string.replace('|', '($SEP$)')
            self.client.send(bytes(f"0|{string}", "utf-8"))

            acknowledgment = self.client.recv(1024).decode()
            if acknowledgment != "ACK":
                print("Error: Client did not acknowledge the message.")


        except socket.error as e:
            if e.errno != 10038 and e.errno != 10054:
                print(f"Socket error: {e}")


    def input(self, string):
        try:
            string = string.replace('|', '($SEP$)')
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
            string = string.replace('|', '($SEP$)')
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
            string = string.replace('|', '($SEP$)')
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
            string = string.replace('|', '($SEP$)')
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
            string = string.replace('|', '($SEP$)')
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
            string = json.dumps(array)

            string = string.replace('|', '($SEP$)') 

            self.client.send(bytes(f"10|{string}", "utf-8"))

            acknowledgment = self.client.recv(1024).decode()
            if acknowledgment != "ACK":
                print("Error: Client did not acknowledge the message.")

        except socket.error as e:
            if e.errno != 10038 and e.errno != 10054:
                print(f"Socket error: {e}")


    def print2dc(self, array):
        try:
            string = json.dumps(array)
            string = string.replace('|', '($SEP$)')
            self.client.send(bytes(f"11|{string}", "utf-8"))
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
            string = string.replace('|', '($SEP$)')
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
            string = string.replace('|', '($SEP$)')
            self.client.send(bytes(f"15|{string}", "utf-8"))

            acknowledgment = self.client.recv(1024).decode()
            if acknowledgment != "ACK":
                print("Error: Client did not acknowledge the message.")

            self.client.close()
            print(f"{self.client_ip} has disconnected from the server at {datetime.datetime.now()}")
        except socket.error as e:
            if e.errno != 10038 and e.errno != 10054:
                print(f"Socket error: {e}")