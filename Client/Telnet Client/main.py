import telnetlib
import socket
import subprocess


# Constants for the BBS System
HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 23  # Telnet default port
ver = "1.5"
device = "Telnet Client"

# Basic authentication (For demonstration purposes, use a static username and password)
VALID_USERNAME = 'user'
VALID_PASSWORD = 'password'

class setup_connection():
    def __init__(self, tn, socket):
        self.tn = tn
        self.socket = socket
        self.line_cache = ''
        self.message = ''

    def print(self, string):
        if '\n' in string or '\r\n' in string: # Multi line have to be processed manually
            lines = string.splitlines()
            for line in lines:
               
                for i in self.line_cache:
                    self.tn.write(b"\033[G")
            
                line_cache = line
                self.tn.write(f'{line}'.encode())
                self.tn.write(b'\r\n')
        else:
            for i in self.line_cache:
                    self.tn.write(b"\033[G") #properly returns the cursor
            
            line_cache = string
            self.tn.write(f'{string}'.encode())
            self.tn.write(b'\r\n')

    def clear(self):
        self.tn.write(b"\033[2J")

    

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
        "light_black": "\033[90m",
        "light_red": "\033[91m",
        "light_green": "\033[92m",
        "light_yellow": "\033[93m",
        "light_blue": "\033[94m",
        "light_magenta": "\033[95m",
        "light_cyan": "\033[96m",
        "light_white": "\033[97m",
        'reset': '\033[0m'
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
        "light_black": "\033[100m",
        "light_red": "\033[101m",
        "light_green": "\033[102m",
        "light_yellow": "\033[103m",
        "light_blue": "\033[104m",
        "light_magenta": "\033[105m",
        "light_cyan": "\033[106m",
        "light_white": "\033[107m",
        'reset': '\033[0m'
    }

    color_code = colors.get(color, colors['reset'])
    background_code = backgrounds.get(background, '')

    return f"{background_code}{color_code}{text}{colors['reset']}"

def dum_ter(server, cSct):

    server_m = server[0]  # the first digit is the mode set by the server.

    data = server[len(server) - 1]
    
    match server_m:
        case "0":
            print(data)
            return None

        case "1":
            user_input = input(data)
            if user_input == "":
                user_input = "None"
            cSct.send(bytes(user_input, "utf-8"))
            return None

        case "2":
            message = data
            cSct.close()
            return "exit"

        case "3":
            clear()
            return None

        case "4":
            print("")
            return None

        case "5":
            user_input = hash_string(str(getpass(data)))
            if user_input == "":
                user_input = "None"
            cSct.send(bytes(user_input, "utf-8"))
            return None

        case "6":

            cSct.send(bytes(str(ver), "utf-8"))
            return None

        case "7":
            os.system(f'curl wttr.in/{load_settings("config.txt")["location"]}')
            return None

        case "8":
            user_input = getpass(data)
            if user_input == "":
                user_input = "None"
            cSct.send(bytes(user_input, "utf-8"))
            return None

        case "9":
            print(colour(data, json.loads(server[1])[0], json.loads(server[1])[1]))
            return None

        case "10":

            screen = json.loads(data)
            print('\n'.join([''.join(['{:4}'.format(item) for item in row])
                             for row in screen]))
            return None

        case "11":

            screen = json.loads(data)
            for row in screen:
                for item in row:
                    char, fg_color, bg_color = item
                    # Print the character with the specified foreground and background colors
                    print(colour(char, fg_color, bg_color), end="")
                print()  # Move to the next line after printing each row
            return None

        case "13":

            #  is_key = kb.is_pressed(data)
            print("Mode 13 unavailable")
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
            print("Out dated client")
            return None       

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
            if message != "":
                print(message)
                message = ""



            ip = connection.input("Server ip:>")
            port = 1998
            server = ip.split(":")

            if ip == "":
                ip = settings["default_server"]
                server = ip.split(":")
                if ip != "":
                    if len(server) == 2:

                        ip = server[0]
                        if ip == "@":
                            ip = "127.0.0.1"

                        port = int(server[1])
                        break
                    break
                else:
                    message = "No default server specified (enter settings to change default server)"

            elif ip == "help":
                message = """Different port other than 1998 use (:), 
    @ for localhost. Also Esc to stop and disconnect server.,
    settings to easily change config
    More info Check the Github README
    """

            elif ip == "credits":
                message = f"""
    Credits
        {colour("Programing", "green")} - {colour("Peter Cakebread", "blue")}
        {colour("Testing", "light_magenta")} - {colour("Reuben D", "light_blue")}
        {colour("Weather (wttr.in)", "yellow")} - {colour("igor_chubin", "light-cyan")}    
                """

            elif ip == "settings":
                message = settings_menu()

            elif ip[len(ip) - 1] == ':':
                message = "Port not specified"

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
                exit(1)

        try:

            mode = 0

            Sct = socket.socket()  # creating the socket
            Sct.connect((ip, port))  # connecting to the server

            while True:
                server_rev = Sct.recv(6000).decode()

                Sct.send("ACK".encode())

                if dum_ter(server_rev.split("|"),Sct) is not None:
                    break

            if load_settings("config.txt")["auto_return"]:
                print(message)
                input("Press Enter to continue...")
            clear()
        except socket.error as e:
            print(f"Socket error: {e}")   
    
    

def start_bbs_server():
    # Create a Telnet server to listen for incoming connections
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"BBS Server running on {HOST}:{PORT}")

    while True:
        # Accept new connections
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")
        client_socket.settimeout(10)  # Set timeout for idle connections

        # Use Telnet protocol to handle the communication
        tn = telnetlib.Telnet()
        tn.sock = client_socket

        connection = setup_connection(tn, socket)

        # Handle the client interaction
        handle_connection(connection)

if __name__ == '__main__':
    start_bbs_server()
