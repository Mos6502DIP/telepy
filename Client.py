import hashlib
import json
import socket
import os
from getpass import getpass
import keyboard as kb

ver = "1.5"
device = "win"

message = ""

def setup():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("No config file detected")
    print(colour("""
88888888888          888          8888888b.
    888              888          888   Y88b
    888              888          888    888
    888      .d88b.  888  .d88b.  888   d88P 888  888
    888     d8P  Y8b 888 d8P  Y8b 8888888P"  888  888
    888     88888888 888 88888888 888        888  888
    888     Y8b.     888 Y8b.     888        Y88b 888
    888      "Y8888  888  "Y8888  888         "Y88888
                                                  888
                                            Y8b d88P
                                             "Y88P"
    Setup Wizard
    """, "green"))
    setup_settings = {}

    setup_settings["location"] = input("Enter Your nearest city this for weather :>")
    user_choice = input("Would you like to test the location? Y/N:>").lower()
    while True:
        if user_choice == "n":
            break

        else:
            os.system("curl wttr.in/" + setup_settings["location"])
            user_choice = input("Is it correct please enter Y or N:>").lower()
            if user_choice == "y":
                break
            else:
                setup_settings["location"] = input("Enter Your nearest city this for weather :>")
                user_choice = "UwU"

    setup_settings["default_server"] = input("""
Enter Your default server to connect to.
(i would recommend server.fractaldev.co) leave blank to select have no default server. 
:>""")

    setup_settings["auto_return"] = False

    write_settings("config.txt", setup_settings)

def hash_string(password):
    return hashlib.sha256(password.encode()).hexdigest()


def load_settings(file):
    try:
        with open(file, "r") as f:
            return json.load(f)

    except FileNotFoundError:
        setup()


def write_settings(file, saved_settings):
    with open(file, "w") as f:
        json.dump(saved_settings, f)


def settings_menu():
    return "under development"
    

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

def  dum_ter(server, cSct):
    global message

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
            os.system("cls")
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
            os.system("curl wttr.in")
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

            is_key = kb.is_pressed(data)

            cSct.send(bytes(str(is_key), "utf-8"))
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


settings = load_settings("config.txt")
os.system("cls")
while True:

    while True:
        settings = load_settings("config.txt")
        os.system("cls")
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
        print(colour("Telepy", "green"), "by", colour("Peter Cakebread", "blue"), f" 2024 v{ver} ({device})")
        if message != "":
            print(message)
            message = ""



        ip = input("Server ip:>")
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
                message = "No default server specified config.txt"

        elif ip == "help":
            message = """Different port other than 1998 use (:), 
            @ for localhost. Also Esc to stop and disconnect server.,
            settings to easily change config
            More info Check the Github README
            Credit to igor_chubin for weather.
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

            if kb.is_pressed("ESC"):
                message = "Disconnected by User"
                break

            Sct.send("ACK".encode())

            if dum_ter(server_rev.split("|"),Sct) is not None:
                break



        os.system("cls")
    except socket.error as e:
        print(f"Socket error: {e}")






