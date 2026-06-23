import telnetlib3 as telnetlib
import socket
import hashlib
import threading
import time
import random
import sys

IAC  = b'\xff'
WILL = b'\xfb'
WONT = b'\xfc'
DO   = b'\xfd'
DONT = b'\xfe'
ECHO = b'\x01'

SGA = b'\x03'

active_connections = []

version = "Telnet-2.1"

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
        if '\n' in string or '\r\n' in string:  # Multi line have to be processed manually
            lines = string.splitlines()
            for line in lines:
                self.tn.write(f'{line}'.encode())
                self.tn.write(b'\r\n')
        else:
            self.tn.write(f'{string}'.encode())
            self.tn.write(b'\r\n')

    def clear(self):
        self.tn.write(b"\033[2J\033[H")

    def bell(self):
        self.tn.write(b"\a")

    def move_cursor(self, row: int, col: int) -> None:
        """Move the terminal cursor to the given row and column (1-based)."""
        self.tn.write(b"\x1b[H")
        bite = f"\x1b[{row};{col}H".encode("UTF-8")
        self.tn.write(bite)
        

    def input(self, string):
       
        self.tn.write(f'{string}'.encode())
        user_input = ""
        while True:
            try:
                char_bytes = self.tn.read_very_eager()
                
                if char_bytes:
                    char = char_bytes.decode('utf-8', errors='ignore')
                    
                    # Handle backspace/delete
                    if char == '\x08' or char == '\x7f':
                        if len(user_input) > 0:
                            user_input = user_input[:-1]
                            # Move cursor back, erase character, move back again
                            self.tn.write(b'\x08 \x08')
                    # Handle carriage return/newline (both \r and \n)
                    elif char == '\r' or char == '\n':
                        self.tn.write(b'\r\n')
                        break

                    elif char == '\r\n':
                        self.tn.write(b'\r\n')
                        break
                    # Handle regular characters
                    else:
                        user_input += char
                        self.tn.write(char.encode())
                        
            except Exception as e:
                pass
            time.sleep(0.01)
        return user_input
    
    def hidden_input(self, string):
        self.tn.write(string.encode())
        user_input = ""
        while True:
            try:
                char_bytes = self.tn.read_very_eager()
                if char_bytes:
                    char = char_bytes.decode('utf-8', errors='ignore')
                    
                    # Handle backspace/delete
                    if char == '\x08' or char == '\x7f':
                        if len(user_input) > 0:
                            user_input = user_input[:-1]
                            # Move cursor back, erase character, move back again
                            self.tn.write(b'\x08 \x08')
                    # Handle carriage return/newline (both \r and \n)
                    elif char == '\r' or char == '\n':
                        self.tn.write(b'\r\n')
                        break

                    elif char == '\r\n':
                        self.tn.write(b'\r\n')
                        break
                    # Handle regular characters - echo as asterisk for password fields
                    else:
                        user_input += char
                        self.tn.write(b'*')
            except Exception as e:
                pass
            time.sleep(0.01)
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
    
    def print(self, string, end="new"):
        if end == "new":
            self.connection.print(string)
        else:
            self.connection.print_no_new_line(string)
        
    def input(self, string):
        user_input = self.connection.input(string)
        if user_input == "":
            user_input = "None"
        return user_input
            
    def close(self, string):
        self.connection.print(string)
        self.socket.close()
        sys.exit()

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
    
    def cursor(self, x, y):
        self.connection.move_cursor(int(y), int(x))

        
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
        
        connection.print(f'Fractal was here!') # fixes a bug do not remove
        connection.clear()
        if connection.terminal_data == b'\r\x00\xff\xfd\x01\xff\xfd\x03\xff\xfb\x03':
            connection.bell()
        connection.print(f'Access Code : {bot_test_code}')
        connection.print(f'{colour("Powered Via Telepy", "green")} by {colour("Peter Cakebread", "blue")} 2026 v{version}')
        
        # Debug: Print what we're waiting for
        print(f"Waiting for access code from {connection.ip}")
        
        user_code = connection.input("Please enter the access code:>")
        print(f"Received code: '{user_code}' from {connection.ip}")  # Debug
        
        if user_code != bot_test_code:
            connection.print(colour('! Invalid access code reconnect and try again !', 'red'))
            connection.socket.close()
            return

        
            

        terminal = dum_ter(connection)
        clientside(terminal)

            

    except socket.timeout:
        print(f"Timeout from IP: {connection.ip}")
        connection.socket.close()
        return
    except Exception as e:
        print(f"Error in handle_connection: {e}")
        import traceback
        traceback.print_exc()
        connection.socket.close()


def start_bbs_server(client_side, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", int(port)))
    server_socket.listen(5)
    print(f"Telnet Server running on port:{port}")
    
    cleanup_thread = threading.Thread(target=clean_dead_threads, daemon=True)
    cleanup_thread.start()
    try:
        while True:
            time.sleep(0.001)
            print('Waiting for Telnet next connection')
            
            client_socket, client_address = server_socket.accept()
            client_socket.sendall(b"\xff\xfb\x01")  # WILL ECHO
            client_socket.sendall(b"\xff\xfb\x03")  # WILL SGA
            client_socket.sendall(b"\xff\xfd\x03")  # DO SGA
        
            data = client_socket.recv(1024)
            accepted_terms = [b'\xff\xfd\x01', b"\xff\xfb\x1f\xff\xfb \xff\xfb\x18\xff\xfb'\xff\xfd\x01\xff\xfb\x03\xff\xfd\x03"]
            if data not in accepted_terms:
                print(data)

            
                
            print(f"Connection from {client_address}")
            client_socket.settimeout(10)

            tn = telnetlib.Telnet()
            tn.sock = client_socket
            connection = setup_connection(tn, client_socket)

            connection.terminal_data = data
            client_thread = threading.Thread(
                target=handle_connection_wrapper,
                args=(connection, client_side),
                name=f"Client-{client_address}"
            )
            
            client_thread.start()

    except Exception as e:
        print(f"Fatal error: {e}")
            