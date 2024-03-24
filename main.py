from TelePy import tp as tp
import threading
import datetime


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

    tp.cls(client)
    c_version = tp.client_version(client)
    tp.printt("Print test!", client)
    tp.printt(f"Client version {c_version}", client)
    user_input = tp.inputt("Enter Normal input:>", client)
    password = tp.password("Enter Password input:>", client)
    hidden = tp.hidden_input("Enter Hidden input:>", client)
    tp.printt(f"Normal input:{user_input} Password input:{password} Hidden input:{hidden}", client)
    txt("Test", client)

    tp.inputt("Press enter!", client)
    tp.cls(client)
    tp.system_command("curl wttr.in", client)

    tp.inputt("Press enter!", client)
    tp.closet(f"Disconnected by user!", client)
    log(log_file, f"{add} has disconnected to server at {time()}")



log_file = f"Telpy server logs for {date()}.txt"  # Change this to your desired file name

Sct = tp.setup_log(log_file)

log(log_file, f"Starting server at {time()}")

while True:
    client_c, add = Sct.accept()
    log(log_file, f"{add} has connected to server at {time()}")
    threading._start_new_thread(clientside, (client_c, add))