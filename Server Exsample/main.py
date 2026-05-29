import TelePy as tp
import threading
import datetime
import time
from os.path import join
import os

os.chdir(os.path.dirname(os.path.abspath(__file__))) #Fixes issues with working directory
info_source = 'server.fractaldev.co:1998'

def screen_generate(x, y, char):
    mem = []
    for i in range(x):
        mem.append([])
        if i % 2 == 1:
            for j in range(y):
                if j % 2 == 1:
                    mem[i].append(char)
                else:
                    mem[i].append(" ")
        else:
            for j in range(y):
                if j % 2 == 1:
                    mem[i].append(" ")
                else:
                    mem[i].append(char)

    return mem

def screen_generate_colour(colours, char):
    mem = []
    for i in range(len(colours)):
        mem.append([])

        for j in range(len(colours)):
            character = [char, colours[j], colours[i]]
            mem[i].append(character)



    return mem



def txt(client, file_name):
    with open(file_name+".txt", "r") as fp:
        lines = fp.readlines()

        for line in lines:
            if line.strip() == "@":
                client.blankline()
            else:
                client.print(line.strip()) 


def date():
    current_datetime = datetime.datetime.now()
    return current_datetime.date()


def time():
    return datetime.datetime.now()


def clientside(client):
    # Basic functions test
    client.cls()
    client.print("Print | test!")
    client.print(f"Version: {client.client_version()}")
   
    user_input = client.input("Enter Normal input:>")
    password = client.password("Enter Password input:>")
    hidden = client.hidden_input("Enter Hidden input:>")
    client.print(f"Normal input:{user_input} Password input:{password} Hidden input:{hidden}")
    txt(client,"Test")

    client.input('Pause Press enter to continue :>')
    
    client.print("Colour test!")

    colours = ["black", "red", "green", "yellow", "blue", "magenta", "cyan",
               "light_red", "light_green", "light_yellow",
               "light_blue", "light_magenta", "light_cyan", "white"]  # compatible colours

    for bg_colour in colours:
        for colour in colours:
            colour_data = [colour, bg_colour]
            client.printc(f"Telepy 2024 (Foreground colour {colour}, Background colour {bg_colour} )", colour_data)
        #client.input('Pause Press enter to continue')

    # 2d array test
    client.print("array test!")

    screen = screen_generate(10,10,"@")

  

    client.print2d(screen)
    # print(screen)
    client.input('Pause Press enter to continue')

    client.print("Colour array test!")

    screen = screen_generate_colour(colours, "@")
    #print(screen)
    client.print2dc(screen)

    client.input("Press Enter to continue...")

    client.print('Getting Sever Sats')
    server_info = tp.get_info(info_source)
    if server_info:
        client.print(f'''Name : {server_info['name']}
    Description : {server_info['description']}
    Uptime : {server_info['uptime']}
    Users Online {server_info['online']}
    Icon :''')
        for line in server_info['icon']:
            client.print(line)
    else:
        client.print(f"Unable to get the server info from ({info_source})")
    client.print(f'Ping:{tp.ping(info_source)}')
    client.print(F'IP:{client.get_ip()}')
    client.input("Press Enter to continue...")
    client.switch("@")

    client.close(f"All test complete and you have been disconnected!")


if __name__ == '__main__':
    tp.start(clientside)  # Starts a server based on the config txt