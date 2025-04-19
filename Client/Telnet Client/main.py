import telnetlib
import socket
import subprocess
from getpass import getpass
import hashlib
import json
import threading  # This is use for multiple clients


# Constants for the BBS System
HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 23  # Telnet default port
ver = "1.5"
device = "Telnet Client"

IAC  = b'\xff'
WILL = b'\xfb'
WONT = b'\xfc'
DO   = b'\xfd'
DONT = b'\xfe'
ECHO = b'\x01'

active_connections = []

class setup_connection():
    def __init__(self, tn, socket):
        self.tn = tn
        self.socket = socket
        self.message = ''
        self.auto_return = False

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

def dum_ter(server, cSct, connection):

    server_m = server[0]  # the first digit is the mode set by the server.

    data = server[len(server) - 1]
    
    match server_m:
        case "0":
            connection.print(data)
            return None

        case "1":
            user_input = connection.input(data)
            if user_input == "":
                user_input = "None"
            cSct.send(bytes(user_input, "utf-8"))
            return None

        case "2":
            connection.message = data
            cSct.close()
            return "exit"

        case "3":
            connection.clear()
            return None

        case "4":
            connection.print("")
            return None

        case "5":
            user_input = hash_string(connection.hidden_input(data))
            if user_input == "":
                user_input = "None"
            cSct.send(bytes(user_input, "utf-8"))
            return None

        case "6":

            cSct.send(bytes(str(ver), "utf-8"))
            return None

        case "7":
            connection.print('Built in weather function disabled')
            return None

        case "8":
            user_input = connection.hidden_input(data)
            if user_input == "":
                user_input = "None"
            cSct.send(bytes(user_input, "utf-8"))
            return None

        case "9":
            connection.print(colour(data, json.loads(server[1])[0], json.loads(server[1])[1]))
            return None

        case "10":

            screen = json.loads(data)
            formatted = render_screen(screen)
            connection.print(formatted)
            return None

        case "11":

            screen = json.loads(data)
            for row in screen:
                for item in row:
                    char, fg_color, bg_color = item
                    # connection.print the character with the specified foreground and background colors
                    connection.print_no_new_line(colour(char, fg_color, bg_color))
                
                connection.new_line()
                
            return None

        case "13":

            #  is_key = kb.is_pressed(data)
            connection.print("Mode 13 unavailable")
            #  cSct.send(bytes(str(is_key), "utf-8"))
            return None

        case "14":

            cSct.send(bytes(str(device), "utf-8"))
            return None

        case "15":
            message = data
            cSct.close()
            return "exit"

        case _:
            connection.print("Out dated client")
            return None       

def handle_connection_wrapper(connection):
    try:
        handle_connection(connection)
    finally:
        # Remove thread from active list when done
        current = threading.current_thread()
        if current in active_connections:
            active_connections.remove(current)

# Function to handle user interaction
def handle_connection(connection):
    
    while True:

        while True:
            connection.clear()
            connection.print('''                                                      
                     ,,                                    
   MMP""MM""YMM    `7MM              `7MM"""Mq.            
   P'   MM   `7      MM                MM   `MM.           
        MM  .gP"Ya   MM  .gP"Ya        MM   ,M9 `7M'   `MF'
        MM ,M'   Yb  MM ,M'   Yb       MMmmdM9    VA   ,V  
        MM 8M""""""  MM 8M""""""       MM          VA ,V   
        MM YM.    ,  MM YM.    ,       MM           VVV    
      .JMML.`Mbmmd'.JMML.`Mbmmd'     .JMML.         ,V     
                                                   ,V      
                                                OOb"       
            ''')
            connection.print(f'{colour("Telepy", "green")} by {colour("Peter Cakebread", "blue")} 2025 v{ver} ({device})')
            if connection.message != "":
                connection.print(connection.message)
                connection.message = ""


            connection.print(f"Online ({online_count()}) Leave blank for Telepy Connect (BBS)")
            ip = connection.input("Server ip:>")
            port = 1998
            server = ip.split(":")

            if ip == "":
                ip = '@'
                server = ip.split(":")
                if ip != "":
                    if len(server) == 2:

                        ip = server[0]
                        if ip == "@":
                            ip = "127.0.0.1"
                        port = int(server[1])
                        break

                    if ip == "@":
                            ip = "127.0.0.1"
                    break
                else:
                    connection.message = "No default server specified (enter settings to change default server)"

            elif ip == "help":
                connection.message = """Different port other than 1998 use (:), 
    @ for localhost. 
    auto_return to enable
    More info Check the Github README
    """

            elif ip == "credits":
                connection.message = f"""
    Credits
        {colour("Programing", "green")} - {colour("Peter Cakebread", "blue")}
        {colour("Testing", "light_magenta")} - {colour("Reuben D", "light_blue")}
        {colour("Weather (wttr.in)", "yellow")} - {colour("igor_chubin", "light-cyan")}    
                """

            elif ip == "settings":
                connection.message = 'Feature Disabled'

            elif ip == 'auto_return':
                if connection.auto_return:
                    connection.auto_return = False
                    connection.message = 'Auto return enabled'
                else:
                    connection.auto_return = True
                    connection.message = 'Auto return disabled'

            elif ip[len(ip) - 1] == ':':
                connection.message = "Port not specified"

            elif len(server) == 2:

                ip = server[0]
                if ip == "@":
                    ip = "127.0.0.1"

                port = int(server[1])
                break

            elif server[0] == "@":

                ip = "127.0.0.1"
                break

            elif ip == "exit":
                connection.tn.close()
            elif ip == "r" or ip == "refresh":
                pass
            else:
                break

        try:

            mode = 0

            Sct = socket.socket()  # creating the socket
            Sct.connect((ip, port))  # connecting to the server

            while True:
                server_rev = Sct.recv(6000).decode()

                Sct.send("ACK".encode())

                if dum_ter(server_rev.split("|"), Sct, connection) is not None:
                    break

            if connection.auto_return:
                connection.print(connection.message)
                connection.input("Press Enter to continue...")
            connection.clear()
        except socket.error as e:
            connection.message = f"Socket error: {e}"

            if connection.auto_return:
                connection.print(connection.message)
                connection.input("Press Enter to continue...")
    
    

def start_bbs_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"BBS Server running on {HOST}:{PORT}")

    while True:
        try:
            client_socket, client_address = server_socket.accept()
            print(f"Connection from {client_address}")
            client_socket.settimeout(10)

            tn = telnetlib.Telnet()
            tn.sock = client_socket
            connection = setup_connection(tn, socket)

            # Start and track the client thread
            client_thread = threading.Thread(
                target=handle_connection_wrapper,
                args=(connection,),
                name=f"Client-{client_address}"
            )
            active_connections.append(client_thread)
            client_thread.start()

        except Exception as e:
            print("Error:", e)


if __name__ == '__main__':
    start_bbs_server()
