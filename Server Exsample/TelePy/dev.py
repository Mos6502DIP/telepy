import sys
import socket
import threading
import json
import time
import datetime



buffer = 0

settings = {}

active_terminal_clients = set()
active_terminal_clients_lock = threading.Lock()

start_time = None

def colour(text, color, background=None):
    colors = {
        "black": "\033[30m",
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
        "white": "\033[37m",

        
        "light_black": "\033[1;30m",
        "light_red": "\033[1;31m",
        "light_green": "\033[1;32m",
        "light_yellow": "\033[1;33m",
        "light_blue": "\033[1;34m",
        "light_magenta": "\033[1;35m",
        "light_cyan": "\033[1;36m",
        "light_white": "\033[1;37m",

        "reset": "\033[0m"
    }
    backgrounds = {
        "black": "\033[40m",
        "red": "\033[41m",
        "green": "\033[42m",
        "yellow": "\033[43m",
        "blue": "\033[44m",
        "magenta": "\033[45m",
        "cyan": "\033[46m",
        "white": "\033[47m",
        "light_black": "\033[1;40m",
        "light_red": "\033[1;41m",
        "light_green": "\033[1;42m",
        "light_yellow": "\033[1;43m",
        "light_blue": "\033[1;44m",
        "light_magenta": "\033[45m",
        "light_cyan": "\033[1;46m",
        "light_white": "\033[1;47m",
        'reset': '\033[0m'
    }

    color_code = colors.get(color, colors['reset'])
    background_code = backgrounds.get(background, '')

    return f"{background_code}{color_code}{text}{colors['reset']}"

def load_config():
    global settings
    with open('config.json', "r") as f:
       settings = json.load(f)

def load_json(name):
    global settings
    with open(f'{name}.json', "r") as f:
        return json.load(f)       

def test():
    print(f"You are using telepy!")


def log(filename, text):
    print(text)
    with open(filename, 'a') as file:
        file.write(text + '\n')


def setup(port):
    global settings
    Sct = socket.socket()  # creating the socket
    
    Sct.bind(("", int(port)))  # Bind port
    Sct.listen(5)  # listens for clients
    print(f'Telepy server started on port:{port}')
    return Sct


def setup_log(port, log_file):
    global settings
    Sct = socket.socket()  # creating the socket
    
    Sct.bind(("", int(port)))  # Bind port
    Sct.listen(5)  # listens for clients
    log(log_file, f'Tele py server started on port:{port}!')
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
        server_config = load_json('info')
        server_info = {
            'name':server_config['server_name'],
            'description':server_config['description'],
            'icon':server_config['icon'],
            'uptime':get_uptime(),
            'online':len(active_terminal_clients)
        }
            
        client_socket.send(bytes(json.dumps(server_info), "utf-8"))

    finally:

        client_socket.close()

def dev(client_side):
    # Loading config
    load_config()
    # Uptime
    start_uptime()

    # Socket setup
    
    
    
    client_obj = Client()

    client_side(client_obj)

def move_cursor(row: int, col: int) -> None:
    """Move the terminal cursor to the given row and column (1-based)."""
    sys.stdout.write(f"\x1b[{row};{col}H")
    sys.stdout.flush()


class Client:

    def __init__(self):
        self.client = "0000000x1"
        self.client_ip = "127.0.0.1"

    def print(self, string):
        print(string)

    def input(self, string):
        data = input(string)
        return data

    def close(self, string):
        print(string)
        print("[DEV] Server closed the connection")
        exit(1)

    def cls(self):
        print("\x1b[2J\x1b[H")


    def blankline(self):
        print(" ")


    def password(self, string):
        self.print("[Dev] Password input")
        data = input(string)
        return data


    def client_version(self):
        return "TelePy-1.9"

    def weather(self):
        print("It's Fooooking windy")


    def hidden_input(self, string):
        self.print("[Dev] Hidden Input")
        data = input(string)
        return data


    def printc(self, string, data):
        

        if len(data) > 1:
            print(colour(string, data[0]))

        else:
            print(colour(string, data[0], data[1]))


    def print2d(self, screen):

        print('\n'.join(''.join('{:4}'.format(item) for item in row) for row in screen))

        


    def print2dc(self, screen):
        for row in screen:
            for item in row:
                char, fg_color, bg_color = item
                # connection.print the character with the specified foreground and background colors
                print(colour(char, fg_color, bg_color), end="")
            
            print(" ")

    
    def switch(self, string):
        print("[Dev] Switching not avlible in dev mode")
        return False
        
    def line(self, string):
        print(string)

    def get_ip(self): # Mode 16
        return "127.0.0.1"
    
    def cursor(self, x, y):
         move_cursor(x, y)
    
    
