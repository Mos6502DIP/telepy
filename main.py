from TelePy import tp as tp
import threading
import datetime



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



def txt(file_name, client_c):
    with open(file_name+".txt", "r") as fp:
        lines = fp.readlines()

        for line in lines:
            if line.strip() == "@":
                tp.blankline(client_c)
            else:
                tp.printt(line.strip(), client_c)


def log(filename, text):
    print(text)
    with open(filename, 'a') as file:
        file.write(text + '\n')


def date():
    current_datetime = datetime.datetime.now()
    return current_datetime.date()


def time():
    return datetime.datetime.now()


def clientside(client, add):
    # Basic functions test
    tp.cls(client)
    c_version = tp.client_version(client)
    tp.printt("Print test!", client)
    tp.printt(f"Client version {c_version}", client)
    if tp.setting("telepi_debug") != "True":
        user_input = tp.inputt("Enter Normal input:>", client)
        password = tp.password("Enter Password input:>", client)
        hidden = tp.hidden_input("Enter Hidden input:>", client)
        tp.printt(f"Normal input:{user_input} Password input:{password} Hidden input:{hidden}", client)
    txt("Test", client)

    # Remote Commands test
    tp.inputt("Press enter!", client)
    tp.cls(client)
    tp.weather(client)
    tp.inputt("Press enter!", client)

    # Colour text test
    tp.cls(client)
    colours = ["black", "red", "green", "yellow", "blue", "magenta", "cyan",
               "light_red", "light_green", "light_yellow",
               "light_blue", "light_magenta", "light_cyan", "white"]  # compatible colours

    for bg_colour in colours:
        for colour in colours:
            colour_data = [colour, bg_colour]
            tp.printc(f"Telepy 2024 (Foreground colour {colour}, Background colour {bg_colour} )", colour_data, client)

    # 2d array test
    tp.inputt("Press enter!", client)
    tp.cls(client)

    screen = screen_generate(10,10,"@")

    tp.print2d(screen, client)

    tp.inputt("Press enter!", client)

    tp.cls(client)

    screen = screen_generate_colour(colours, "@")

    tp.print2dc(screen, client)

    tp.inputt("Press enter!", client)








    tp.closet(log_file,f"Disconnected by user!", client, add)




log_file = f"Telpy server logs for {date()}.txt"  # Change this to your desired file name

Sct = tp.setup_log(log_file)

log(log_file, f"Starting server at {time()}")

while True:
    client_c, add = Sct.accept()
    log(log_file, f"{add} has connected to server at {time()}")
    threading._start_new_thread(clientside, (client_c, add))