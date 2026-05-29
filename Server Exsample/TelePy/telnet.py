import telnetlib3 as telnetlib
import socket
import hashlib
import threading  # This is use for multiple clients
import time
import random
import sys

IAC  = b'\xff'
WILL = b'\xfb'
WONT = b'\xfc'
DO   = b'\xfd'
DONT = b'\xfe'
ECHO = b'\x01'

active_connections = []

version = "Telnet-1.9"

class setup_connection():
    def __init__(self, tn, socket):
        ip, port = tn.sock.getpeername()
        self.tn = tn
        self.socket = socket
        self.message = ''
        self.auto_return = False
        self.ip = ip
        self.port = port

    def print(self, string):
        if '\n' in string or '\r\n' in string: # Multi line have to be processed manually
            lines = string.splitlines()
            for line in lines:
                self.tn.write(f'{line}'.encode())
                self.tn.write(b'\r\n')
        else:
            self.tn.write(f'{string}'.encode())
            self.tn.write(b'\r\n')

    def clear(self):
        self.tn.write(b"\033[2J")

    def input(self, string):
        self.tn.write(f'{string}'.encode())
        return self.tn.read_until(b"\r\n").decode('utf-8').strip()
    
    def hidden_input(self, string):
        self.tn.write(string.encode())
        user_input = self.tn.read_until(b"\r\n").decode('utf-8').strip()

        # Overwrite line with asterisks or clear it
        erase_line = '\r' + ' ' * (len(string) + len(user_input)) + '\r'
        self.tn.write(b'\033[1A')
        self.tn.write(erase_line.encode())
        self.tn.write(f'{string}{"*" * len(user_input)}\r\n'.encode())

        return user_input
    
    def print_no_new_line(self, string):
        self.tn.write(f'{string}'.encode())
   
    def new_line(self):
        self.tn.write(b'\r\n')


def render_screen(screen):
    return '\n'.join(''.join('{:4}'.format(item) for item in row) for row in screen)

def online_count():
    # Clean up finished threads
    for thread in active_connections[:]:
        if not thread.is_alive():
            active_connections.remove(thread)
    return len(active_connections)

def clean_dead_threads():
    while True:
        time.sleep(5)
        for thread in active_connections[:]:
            if not thread.is_alive():
                active_connections.remove(thread)

def hash_string(password):
    return hashlib.sha256(password.encode()).hexdigest()

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

class dum_ter:

    def __init__(self, connection):
        # Initial D setup
        self.connection = connection
        self.ip = connection.ip
        self.socket = connection.socket
    
    def print(self, string):
        self.connection.print(string)
        
    def input(self, string):
        
        user_input = self.connection.input(string)
        if user_input == "":
            user_input = "None"
        return user_input
            
    def close(self, string):
        self.connection.print(string)
        self.socket.close()
        sys.exit() # This is the wrong way to implement this but it works (Hopefully) :3
        

    def cls(self):
        self.connection.clear()

    def blankline(self):
        self.connection.new_line() 

    def password(self, string):
        user_input = self.connection.hidden_input(string)
        if user_input == "":
            user_input = "None"
        return user_input
                    
    def weather(self):
        self.connection.print('Computer Says No!')
    
    def client_version(self):
        return version
    
    def hidden_input(self, string):
        user_input = self.connection.hidden_input(string)
        if user_input == "":
            user_input = "None"
        return user_input
 
    def printc(self, string, data):
        if len(data) > 1:
            self.connection.print(colour(string, data[0]))

        else:
            self.connection.print(colour(string, data[0], data[1]))
    
    def print2d(self, screen):
        formatted = render_screen(screen)
        self.connection.print(formatted)
        

            

    def print2dc(self, screen):
        for row in screen:
            for item in row:
                char, fg_color, bg_color = item
                # connection.print the character with the specified foreground and background colors
                self.connection.print_no_new_line(colour(char, fg_color, bg_color))
            
            self.connection.new_line()
                
    def get_ip(self):
        return self.ip

    def switch(self, ip):
        self.connection.print(f'Server has attempted to switch to :{ip} Unable due to telnet.')
        return False
            

        
def handle_connection_wrapper(connection, clientside):
    try:
        handle_connection(connection, clientside)
    finally:
        connection.socket.close()

# Function to handle user interaction
def handle_connection(connection, clientside):
    # New code base
    try:
        bot_test_code = str(random.randint(100000, 999999))
        connection.socket.settimeout(10)
        connection.print(f'Access Code : {bot_test_code}')
        connection.print(f'{colour("Powered Via Telepy", "green")} by {colour("Peter Cakebread", "blue")} 2026 v{version}')
        user_code = connection.input("Please enter the access code:>")
        if user_code != bot_test_code:
            connection.print(colour('! Invalid access code reconnect and try again !', 'red'))
            connection.socket.close()

        terminal = dum_ter(connection)
        clientside(terminal)

            

    except socket.timeout:
        print(connection.ip)
        connection.socket.close()
        








    
    
    

def start_bbs_server(client_side, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", int(port)))
    server_socket.listen(5)
    print(f"Telnet Server running on port:{port}")
    
    cleanup_thread = threading.Thread(target=clean_dead_threads, daemon=True)
    cleanup_thread.start()
    while True:
        time.sleep(0.001)
        print('Waiting for Telnet next connection')
        try:
            client_socket, client_address = server_socket.accept()
            print(f"Connection from {client_address}")
            client_socket.settimeout(10)

            tn = telnetlib.Telnet()
            tn.sock = client_socket
            connection = setup_connection(tn, client_socket)

            client_thread = threading.Thread(
                target=handle_connection_wrapper,
                args=(connection, client_side),
                name=f"Client-{client_address}"
            )
            
            client_thread.start()

        except Exception as e:
            print(f"Fatal error: {e}")
            raise


