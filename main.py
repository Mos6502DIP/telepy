from TelePy import tp as tp
import threading
import datetime
import time
from os.path import join


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
    client.print("Print test!")
    client.print(f"Client version {c_version}" )
    if tp.setting("telepi_debug") != "True":
        user_input = client.input("Enter Normal input:>")
        password = client.password("Enter Password input:>")
        hidden = client.hidden_input("Enter Hidden input:>")
        client.print(f"Normal input:{user_input} Password input:{password} Hidden input:{hidden}")
    txt(client,"Test")

    # Remote Commands test
    client.print("Weather")

    client.weather()

    client.print("Colour test!")

    colours = ["black", "red", "green", "yellow", "blue", "magenta", "cyan",
               "light_red", "light_green", "light_yellow",
               "light_blue", "light_magenta", "light_cyan", "white"]  # compatible colours

    for bg_colour in colours:
        for colour in colours:
            colour_data = [colour, bg_colour]
            client.printc(f"Telepy 2024 (Foreground colour {colour}, Background colour {bg_colour} )", colour_data)

    # 2d array test
    client.print("array test!")

    screen = screen_generate(10,10,"@")

    client.print2d(screen)


    client.print("Colour array test!")

    screen = screen_generate_colour(colours, "@")

    client.print2dc(screen)

    client.input("Press Enter to continue...")

    client.closet(log_file,f"Disconnected by user!")




log_file = join("Logs", f"Telpy server logs for {date()}.txt")  # Change this to your desired file name

Sct = tp.setup_log(log_file)

log(log_file, f"Starting server at {time()}")

while True:
    client_c, add = Sct.accept()
    tp.log(log_file, f"{add} has connected to server at {time()}")
    client = tp.Client(client_c, add)
    threading._start_new_thread(clientside, (client,))
