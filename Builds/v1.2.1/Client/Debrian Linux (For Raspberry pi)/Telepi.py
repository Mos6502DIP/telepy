import hashlib
import socket
import os
from getpass import getpass

try:
    from termcolor import colored


except ImportError:
    print("termcolor not found")
    if input("Automatically install termcolor? [Y/n] ").lower() == "y":
        print("Installing pip")
        os.system("sudo apt install python3 python3-pip")
        print("Installing termcolor! (Be patient)")
        os.system("pip3 install termcolor")
        print("Relaunch Telepi.")
        exit(2)


ver = "1.2.1"


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



def dum_ter(server, cSct):

    server_m = server[0]  # the first digit is the mode set by the server.

    data =  server[len(server)-1]

    if server_m == "0":
        print(data)

        return None
    elif server_m == "1":
        user_input = input(data)
        if user_input == "":
            user_input = "None"
        cSct.send(bytes(user_input, "utf-8"))
        return None
    elif server_m == "2":
        print(data)
        cSct.close()
        input("Press enter to return to prompt!")
        return "exit"
    elif server_m == "3":
        os.system("clear")
        return None
    elif server_m == "4":
        print("")
        return None
    elif server_m == "5":
        user_input = hash_string(str(getpass(data)))
        if user_input == "":
            user_input = "None"
        cSct.send(bytes(user_input, "utf-8"))
        return None

    elif server_m == "6":
        cSct.send(bytes(str(ver), "utf-8"))
        return None

    elif server_m == "7":
        if setting("commands") == "True":
            os.system(data)
        else:
            print(f"Command({data}) has not been allowed to run.")
        return None

    elif server_m == "8":
        user_input = getpass(data)
        if user_input == "":
            user_input = "None"
        cSct.send(bytes(user_input, "utf-8"))
        return None

    elif server_m == "9":
        print(colored(data, server[1]))
        return None


    else:
        print("Out dated client")
        return None

os.system("clear")
while True:

    while True:
        print('''
                                                          
                  ,,                              
MMP""MM""YMM    `7MM              `7MM"""Mq.`7MMF'
P'   MM   `7      MM                MM   `MM. MM  
     MM  .gP"Ya   MM  .gP"Ya        MM   ,M9  MM  
     MM ,M'   Yb  MM ,M'   Yb       MMmmdM9   MM  
     MM 8M""""""  MM 8M""""""       MM        MM  
     MM YM.    ,  MM YM.    ,       MM        MM  
   .JMML.`Mbmmd'.JMML.`Mbmmd'     .JMML.    .JMML.
                                                  
                                                  
        ''')



        print(colored("Telepi", "green"), "by", colored("Peter Cakebread", "blue"), f" 2024 v{ver}")

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

            server_rev = Sct.recv(1024).decode()
            Sct.send("ACK".encode())
            if dum_ter(server_rev.split("|"), Sct) is not None:
                break
        os.system("clear")
    except socket.error as e:
        print(f"Socket error: {e}")




