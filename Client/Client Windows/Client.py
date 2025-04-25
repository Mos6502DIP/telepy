import hashlib
import json
import socket
import os
import time
from getpass import getpass
import keyboard
# Telepy Copyright 2025 Peter Cakebread

v_settings = {'auto_return', 'location', 'default_server', 'switch_consent'} # Ensures that the client settings json is up to date

ver = "1.8"
device = "win"

message = ""

ip = ''

def select_weather():

    location = input("Enter Your nearest city this for weather :>")
    user_choice = input("Would you like to test the location? Y/N:>").lower()
    while True:
        if user_choice == "n":
            return location

        else:

            os.system("curl wttr.in/" + location)
            time.sleep(0.5)
            user_choice = input("Is it correct please enter Y or N:>").lower()
            if user_choice == "y":
                return location
            else:
                location = input("Enter Your nearest city this for weather :>")
                user_choice = "UwU"


def setup():
    global message

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

    setup_settings["location"] = select_weather()

    setup_settings["default_server"] = input("""Enter Your default server to connect to (i would recommend server.fractaldev.co).
Leave blank to select have no default server.:>""")

    setup_settings["auto_return"] = False

    write_settings("config.txt", setup_settings)

    message = f"Welcome to Tele Py :3"
    input("Saved! Press Enter to continue you can changes these at anytime just enter `settings` at the prompt...")


def hash_string(password):
    return hashlib.sha256(password.encode()).hexdigest()


def load_settings(file):
    try:
        with open(file, "r") as f:
            settings = json.load(f)

        for setting in settings:
            if setting not in v_settings:
                print(f'Setting {setting} Not Found')
    except FileNotFoundError:
        setup()


def write_settings(file, saved_settings):
    with open(file, "w") as f:
        json.dump(saved_settings, f)


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def settings_menu():
    clear()
    settings_temp = load_settings("config.txt")
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
1. Weather Location : {settings_temp["location"]}
2. Default Server : {settings_temp["default_server"]}
3. Auto-Return : {settings_temp["auto_return"]}
4. Save and exit
        """)

    update_menu()
    while True:
        choice = input("Choose an option: ").strip()

        if choice == "1":

            settings_temp["location"] = select_weather()
        elif choice == "2":

            settings_temp["default_server"] = input("Enter new default server: ").strip()
        elif choice == "3":

            settings_temp["auto_return"] = not settings_temp["auto_return"]
        elif choice == "4":
            write_settings("config.txt", settings_temp)
            print("Settings Saved.")
            return "Settings saved"
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
            print(f'Server Switching to {data}')
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
        case _:
            print("Out dated client")
            return None


settings = load_settings("config.txt")
clear()

while True:

    while True:
        settings = load_settings("config.txt")
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
        print(colour("Telepy", "green"), "by", colour("Peter Cakebread", "blue"), f" 2025 v{ver} ({device})")
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
                if ip == "@":
                            ip = "127.0.0.1"
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

        else:
            break

    try:
        mode = 0
        Sct = socket.socket()
        Sct.connect((ip, port))

        while True:
            if keyboard.is_pressed("ESC"):
                message = "Disconnected by User"
                Sct.close()
                break

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


