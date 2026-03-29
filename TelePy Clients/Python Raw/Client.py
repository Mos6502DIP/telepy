import hashlib
import json
import socket
import os
import time
from getpass import getpass
# import keyboard
import sys
# Telepy Copyright 2026 Peter Cakebread

v_settings = {'auto_return', 'default_server', 'switch_consent'} # Ensures that the client settings json is up to date

ver = "TelePy-1.9"

message = ''

jar_file = 'jar.json'
ip = ''

settings = {}

if getattr(sys, 'frozen', False): # Py installer fix
    # Running as a bundled executable
    app_dir = os.path.dirname(sys.executable)
else:
    # Running in development
    app_dir = os.path.dirname(os.path.abspath(__file__))

os.chdir(app_dir) # Fixes issues related to files being incorrect

def info(server_ip, port):
    try:
        Sct = socket.socket()
        Sct.connect((server_ip, port))
        Sct.send(bytes('json', "utf-8"))
        server_info = json.loads(Sct.recv(6000).decode())
        Sct.close()
        output = f'''Name : {server_info['name']}
Description : {server_info['description']}
Uptime : {server_info['uptime']}
Users Online {server_info['online']}
Icon :'''
        for line in server_info['icon']:
            output += f'\n{line}'

        return output
    except (socket.timeout, socket.error) as e:
        return f"Error: {e}"
def ping(server_ip, port):
    try:
        
        times = []
        

        for i in range(1, 6):
            Sct = socket.socket()
            Sct.settimeout(5)  # Optional: timeout after a few seconds
            
            print(f'Sending Ping {i} to {server_ip}:{port}', end='')
            start_time = time.time()
            Sct.connect((server_ip, port))
            Sct.send(b'ping')  # Send "ping"
            
            response = Sct.recv(1024).decode()
            end_time = time.time()

            Sct.close()

            if response.strip().lower() == "pong":
                ping_ms = (end_time - start_time) * 1000  # Convert to milliseconds
                print(f'  Responded with a Ping:{round(ping_ms, 2)}ms')
                times.append(round(ping_ms, 2))
            else:
                print(f'Ping {i} had a Invalid response')  # Unexpected response
                times.append(100)

            time.sleep(0.5) # Avoids over whelming the server

        avg = round(sum(times) / len(times), 4)
        print(f'Ping stats Avg:{avg}ms, Longest:{max(times)}ms, Quickest:{min(times)}')
        input('Press Enter to return ...')
        return f'Ping stats Avg:{avg}ms, Longest:{max(times)}ms, Quickest:{min(times)}'
    except (socket.timeout, socket.error) as e:
        return f"Error: {e}"


def setup():
    global message
    global settings
    os.system('cls' if os.name == 'nt' else 'clear')
    print("No config file detected")
    print(colour("""Making Config File
    """, "green"))
    setup_settings = {}


    setup_settings["default_server"] = ''

    setup_settings["auto_return"] = False
    setup_settings['switch_consent'] = False

    write_settings("config.txt", setup_settings)
    setup_settings = settings
    message = f"Welcome to Tele Py :3"
    easter = input("Welcome to the world of Telepy. Press enter to Jack in to the Matrix ... ") # We have fun around here at telepy HQ
    easter = easter.lower()
    if easter == 'neo':
        message = 'This will feel a little weird.'
    elif easter == 'joshua':
        message = 'Would you like to play a game of chess?'
    elif easter == 'blahaj':
        message = 'Blahaj is Babe UwU'
    elif len(easter) > 0:
        message = '''It did say just press enter but you chose to input something. 
But me telling you not to shows there is logic that will detect if strings have been entered.
If you find them all with out looking in the source code. Something cool will happen if you 
do, when that happens email me and you get a prize!'''
        # If you the person who decide to look for it in the source code you can now fix it pls. Or add something to happen.

def hash_string(password):
    return hashlib.sha256(password.encode()).hexdigest()


def load_settings(file):
    global settings
    try:
        with open(file, "r") as f:
            settings = json.load(f)

        for setting in settings:
            if setting not in v_settings:
                print(f'Setting {setting} Not Found')
                input(f'Setup Will now start')
                setup()
    except FileNotFoundError:
        setup()

def load_biscuit(server):
    
    try:
        with open(jar_file, "r") as f:
            jar = json.load(f)

        if server in jar:
            return jar[server]['biscuit']
        
        else:
            return 'None'
    except FileNotFoundError:
        return 'None'

def save_biscuit(server, biscuit):
    try:
        with open(jar_file, "r") as f:
            jar = json.load(f)

        if server in jar:
            jar[server]['biscuit'] = biscuit
        
        else:
            return 'None'
    except FileNotFoundError:
        return 'None'

def write_settings(file, saved_settings):
    with open(file, "w") as f:
        json.dump(saved_settings, f)


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def settings_menu():
    global settings
    clear()
    settings_temp = settings
    logo = """                                                                  
 ███████╗███████╗████████╗████████╗██╗███╗   ██╗ ██████╗ ███████╗ 
 ██╔════╝██╔════╝╚══██╔══╝╚══██╔══╝██║████╗  ██║██╔════╝ ██╔════╝ 
 ███████╗█████╗     ██║      ██║   ██║██╔██╗ ██║██║  ███╗███████╗ 
 ╚════██║██╔══╝     ██║      ██║   ██║██║╚██╗██║██║   ██║╚════██║ 
 ███████║███████╗   ██║      ██║   ██║██║ ╚████║╚██████╔╝███████║ 
 ╚══════╝╚══════╝   ╚═╝      ╚═╝   ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝ 

"""

    def update_menu():
        print(f"""
{colour(logo, "white", "blue")}
Settings Menu (use numbers to navigate, Enter to select)
1. Default Server : {settings_temp["default_server"]}
2. Auto-Return : {settings_temp["auto_return"]}
3. Switch Concent : {settings_temp['switch_consent']}
4. Save and exit
        """)

    update_menu()
    while True:
        choice = input("Choose an option: ").strip()

        
        if choice == "1":

            settings_temp["default_server"] = input("Enter new default server: ").strip()
        elif choice == "2":

            settings_temp["auto_return"] = not settings_temp["auto_return"]

        elif choice == "3":

            settings_temp["switch_consent"] = not settings_temp["switch_consent"]
        elif choice == "4":
            write_settings("config.txt", settings_temp)
            settings = settings_temp
            print("Settings Saved.")
            return "Settings saved" # F windows
        else:
            print("Invalid option, please try again.")

        # Clear screen and update the menu after making changes
        clear()
        update_menu()


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
    global message
    global ip
    global settings

    server_m = server[0]  # the first digit is the mode set by the server.

    data = server[len(server) - 1]

    data = data.replace('($SEP$)', '|')
    data = data.replace('\n', '')
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
            user_input = getpass(data)
            if user_input == "":
                user_input = "None"
            cSct.send(bytes(user_input, "utf-8"))
            return None

        case "6":

            cSct.send(bytes(str(ver), "utf-8"))
            return None

        case "7":
            print("It's Raining because we be in the UK")
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

            print('Mode not in use')

        case "13":

            #  is_key = kb.is_pressed(data)
            print("Mode 13 unavailable")
            #  cSct.send(bytes(str(is_key), "utf-8"))
            return None

        case "14":

            cSct.send(bytes(str(ver), "utf-8"))
            return None

        case "15":
            message = data
            print(f'Server Switching to {data}')
            if settings['switch_consent']:
                cSct.send(bytes('switch', "utf-8"))
                cSct.close()
                ip = data
                message = 'server change'
                return "exit"
            else:
                choice =  input("Accept (y/n) :>").lower()
                if choice == 'y':
                    cSct.send(bytes('switch', "utf-8"))
                    cSct.close()
                    ip = data
                    message = 'server change'
                    return "exit"
                else:
                    cSct.send(bytes('deny', "utf-8"))
                    return None
                
        case "16":
            pass

        case "19":
            print(data, end="")
            return None
        
        case _:
            print(f"Invalid Head / Out dated client. Head/Mode received ({server_m})")
            return None


load_settings("config.txt")
clear()
load_settings("config.txt")
while True:

    while True:
        
        clear()
        print('''                                                      
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
        print(colour("Telepy", "green"), "by", colour("Peter Cakebread", "blue"), f" 2025 v{ver}")
        if message != "":
            if message == 'server change':
                print(f'Server switching to {ip}')
                
            else:
                print(message)
                message = ""


        if message != 'server change':
            ip = input("Server ip:>")

        else:
            message = ""
        port = 1998
        ip = ip.strip()
        commands = ip.split(" ")
        server = ip.split(":")

        # If input is empty, use default server
        if ip == "":
            ip = settings.get("default_server", "")
            if not ip:
                message = "No default server specified (enter settings to change default server)"
            else:
                server = ip.split(":")
                if len(server) == 2:
                    ip, port_str = server
                    ip = "127.0.0.1" if ip == "@" else ip
                    port = int(port_str)
                elif ip == "@":
                    ip = "127.0.0.1"
            break

        # Info command
        elif commands[0] == "info":
            if len(commands) == 2:
                target = commands[1]
                parts = target.split(':')
                server_ip = parts[0]
                port = int(parts[1]) if len(parts) == 2 else 1998
                message = info(server_ip, port)
            else:
                message = 'Invalid info command.'

        # Ping command
        elif commands[0] == "ping":
            if len(commands) == 2:
                target = commands[1]
                if ':' in target:
                    server_ip, port_str = target.split(':', 1)
                    port = int(port_str)
                else:
                    server_ip = target
                    port = 1998

                if not server_ip:
                    message = 'Invalid IP address.'
                else:
                    message = ping(server_ip, port)
            else:
                message = 'Invalid ping command.'

        # Help command
        elif ip == "help":
            message = (
                "Different port other than 1998 use (:),\n"
                "@ for localhost. Esc to stop and disconnect server.\n"
                "Settings to easily change config\n"
                "ping to get server response time eg (ping example.com)\n"
                "info to get server info eg (info example.com)\n"
                "More info: Check the Github README"
            )

        # Credits command
        elif ip == "credits":
            message = f"""Credits
{colour("Programming", "green")} - {colour("Peter Cakebread", "blue")}
{colour("Emotional Support Animal", "yellow")} - {colour("Blahaj", "light_blue")}
    
            """

        # Settings command
        elif ip == "settings":
            message = settings_menu()

        # Catch missing port after colon
        elif ip.endswith(":"):
            message = "Port not specified"

        # Handle raw IP:PORT
        elif len(server) == 2:
            ip, port_str = server
            ip = "127.0.0.1" if ip == "@" else ip
            port = int(port_str)
            break

        # Handle shorthand localhost
        elif ip == "@":
            ip = "127.0.0.1"
            break

        # Exit command
        elif ip == "exit":
            exit(1)


        # Fallback (breaks out of loop)
        else:
            break

    try:
        mode = 0
        Sct = socket.socket()
        Sct.connect((ip, port))
        Sct.send(bytes('terminal', "utf-8")) # Tells the server it wants a terminal
        while True:
            
            try:
                server_rev = Sct.recv(6000).decode()
                if not server_rev:
                    message = "Server closed connection"
                    Sct.close()
                    break

                Sct.send("ACK".encode())
                dum_ter_response = dum_ter(server_rev.split("|"), Sct)

                if dum_ter_response == 'exit':
                    Sct.close()
                    break

            except socket.error as e:
                message = f"Socket error inside loop: {e}"
                try:
                    Sct.close()
                except:
                    pass
                break
    except socket.error as e:
        message = f"Socket error: {e}"


