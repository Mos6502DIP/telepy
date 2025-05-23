import TelePy as tp
import threading
import datetime
import time
from os.path import join
import os

os.chdir(os.path.dirname(os.path.abspath(__file__))) #Fixes issues with working directory


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


def log(filename, text):
    print(text)
    with open(filename, 'a') as file:
        file.write(text + '\n')


def date():
    current_datetime = datetime.datetime.now()
    return current_datetime.date()


def time():
    return datetime.datetime.now()


def clientside(client):
    # Basic functions test
    client.cls()
    c_version = client.client_version()
    d_version = client.device()
    client.print("Print | test!")
    client.print(f"Version: {c_version}")
    client.print(f"Device Info {d_version}" )
    
    user_input = client.input("Enter Normal input:>")
    password = client.password("Enter Password input:>")
    hidden = client.hidden_input("Enter Hidden input:>")
    client.print(f"Normal input:{user_input} Password input:{password} Hidden input:{hidden}")
    txt(client,"Test")

    client.input('Pause Press enter to continue :>')
    # Remote Commands test
    client.print("Weather")

    client.weather()
    client.input('Pause Press enter to continue')
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

    print(screen)

    client.print2d(screen)
    client.input('Pause Press enter to continue')

    client.print("Colour array test!")

    screen = screen_generate_colour(colours, "@")
    print(screen)
    client.print2dc(screen)

    client.input("Press Enter to continue...")

    client.print('Getting Sever Sats')
    server_info = tp.get_info('127.0.0.1:2001')

    client.print(f'''Name : {server_info['name']}
Description : {server_info['description']}
Uptime : {server_info['uptime']}
Users Online {server_info['online']}
Icon :''')
    for line in server_info['icon']:
        client.print(line)
    client.print(f'Ping:{round(tp.ping("127.0.0.1:2001"), 2)}')
    client.get_ip()
    client.input("Press Enter to continue...")
    client.switch("server.fractaldev.co")

    client.closet_log(log_file,f"Disconnected by user!")


if __name__ == '__main__':
    log_file = join("Logs", f"Telpy server logs for {date()}.txt")  # Change this to your desired file name

    log(log_file, f"Starting server at {time()}")

    tp.start(clientside, log_file=log_file)  # Starts a server based on the config txt