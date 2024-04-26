import hashlib
import json
import socket
import os
from getpass import getpass
from termcolor import colored

ver = "1.3.1"


def hash_string(password):
    return hashlib.sha256(password.encode()).hexdigest()


def setting(setting:str):
    try:
        with open("config.txt") as fp:
            lines = fp.readlines()
            for line in lines:
                if line.strip()[0] != "#":
                    setting_line = line.strip().split("=")
                    if setting_line[0] == setting:
                        return setting_line[1]

    except:
        print("No config.txt")


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
            print(data)
            cSct.close()
            input("Press enter to return to prompt!")
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

        case _:
            print("Out dated client")
            return None

os.system("cls")
while True:

    while True:
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
        print(colour("Telepi", "green"), "by", colour("Peter Cakebread", "blue"), f" 2024 v{ver}")
        ip = input("Server ip:>")
        port = 1998
        server = ip.split(":")

        if ip == "":
            ip = setting("default_server")
            server = ip.split(":")
            if ip != "None":
                if len(server) == 2:

                    ip = server[0]
                    if ip == "@":
                        ip = "127.0.0.1"

                    port = int(server[1])
                    break
                break
            else:
                print("No default server specified config")

        elif ip[len(ip) - 1] == ':':
            print("Port not specified")

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
        Sct = socket.socket()  # creating the socket
        Sct.connect((ip, port))  # connecting to the server

        while True:

            server_rev = Sct.recv(6000).decode()

            Sct.send("ACK".encode())
            if dum_ter(server_rev.split("|"), Sct) is not None:
                break
        os.system("cls")
    except socket.error as e:
        print(f"Socket error: {e}")






