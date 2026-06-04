import telnetlib3 as telnetlib
import socket
import hashlib
import threading
import time
import random
import sys
import logging
import signal
import sys as _sys

from ._colour import colour

IAC  = b'\xff'
WILL = b'\xfb'
WONT = b'\xfc'
DO   = b'\xfd'
DONT = b'\xfe'
ECHO = b'\x01'

active_connections = []
active_connections_lock = threading.Lock()

version = "Telnet-2.0"
shutdown_requested = False

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def signal_handler(signum, frame):
    global shutdown_requested
    logger.info("Signal received, initiating shutdown...")
    shutdown_requested = True
    _sys.exit(0)

signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

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
    with active_connections_lock:
        return len([t for t in active_connections if t.is_alive()])

def clean_dead_threads():
    while not shutdown_requested:
        time.sleep(5)
        with active_connections_lock:
            dead = [t for t in active_connections if not t.is_alive()]
            for t in dead:
                active_connections.remove(t)
            if dead:
                logger.info(f"Cleaned up {len(dead)} dead threads")

def hash_string(password):
    return hashlib.sha256(password.encode()).hexdigest()



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
        try:
            self.socket.close()
        except Exception:
            pass
        

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
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", int(port)))
    server_socket.listen(5)
    logger.info(f"Telnet Server running on port:{port}")
    
    cleanup_thread = threading.Thread(target=clean_dead_threads, daemon=True)
    cleanup_thread.start()
    while not shutdown_requested:
        try:
            client_socket, client_address = server_socket.accept()
            logger.info(f"Connection from {client_address}")
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
            with active_connections_lock:
                active_connections.append(client_thread)

        except Exception as e:
            logger.error(f"Telnet server error: {e}")


