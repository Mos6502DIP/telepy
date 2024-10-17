import socket
import datetime
import time
import json
import sys

buffer = 0


def setting(setting: str):

    with open("server_config.txt") as fp:
        lines = fp.readlines()
        for line in lines:
            if line.strip()[0] != "#":
                setting_line = line.strip().split("=")
                if setting_line[0] == setting:
                    return setting_line[1]


def test():
    print(f"You are using telepy!")


def log(filename, text):
    print(text)
    with open(filename, 'a') as file:
        file.write(text + '\n')


def setup():

    Sct = socket.socket()  # creating the socket
    ports = int(setting("port"))
    Sct.bind(("", int(ports)))  # Bind port
    Sct.listen(int(setting("listen")))  # listens for clients
    print(f'Tele py server started on port:{ports} and listening for {setting("listen")} Clients!')
    return Sct


def setup_log(log_file):

    Sct = socket.socket()  # creating the socket
    ports = setting("port")
    Sct.bind(("", int(ports)))  # Bind port
    Sct.listen(int(setting("listen")))  # listens for clients
    log(log_file, f'Tele py server started on port:{ports} and listening for {setting("listen")} Clients!')
    return Sct

class Client:

    def __init__(self, client_id, client_ip):
        self.client = client_id
        self.client_ip = client_ip

    def print(self, string):
        try:
            time.sleep(buffer)
            self.client.send(bytes(f"0|{string}", "utf-8"))

            acknowledgment = self.client.recv(1024).decode()
            if acknowledgment != "ACK":
                print("Error: Client did not acknowledge the message.")


        except socket.error as e:
            if e.errno != 10038 and e.errno != 10054:
                print(f"Socket error: {e}")


    def input(self, string):
        try:
            time.sleep(buffer)
            self.client.send(bytes(f"1|{string}", "utf-8"))

            acknowledgment = self.client.recv(1024).decode()
            if acknowledgment != "ACK":
                print("Error: Client did not acknowledge the message.")

            return self.client.recv(1024).decode()
        except socket.error as e:
            if e.errno != 10038 and e.errno != 10054:
                print(f"Socket error: {e}")

            return None


    def closet_log(self, log_file, string):
        try:
            time.sleep(buffer)
            self.client.send(bytes(f"2|{string}", "utf-8"))

            acknowledgment = self.client.recv(1024).decode()
            if acknowledgment != "ACK":
                print("Error: Client did not acknowledge the message.")

            self.client.close()
            log(log_file, f"{self.client_ip} has disconnected from the server at {datetime.datetime.now()}")
        except socket.error as e:
            if e.errno != 10038 and e.errno != 10054:
                print(f"Socket error: {e}")


    def cls(self):
        try:
            time.sleep(buffer)
            self.client.send(bytes(f"3|", "utf-8"))

            acknowledgment = self.client.recv(1024).decode()
            if acknowledgment != "ACK":
                print("Error: Client did not acknowledge the message.")

        except socket.error as e:

            if e.errno != 10038 and e.errno != 10054:
                print(f"Socket error: {e}")


    def blankline(self):
        try:
            time.sleep(buffer)
            self.client.send(bytes(f"4|", "utf-8"))

            acknowledgment = self.client.recv(1024).decode()
            if acknowledgment != "ACK":
                print("Error: Client did not acknowledge the message.")

        except socket.error as e:
            if e.errno != 10038 and e.errno != 10054:
                print(f"Socket error: {e}")


    def password(self, string):
        try:
            time.sleep(buffer)
            self.client.send(bytes(f"5|{string}", "utf-8"))

            acknowledgment = self.client.recv(1024).decode()
            if acknowledgment != "ACK":
                print("Error: Client did not acknowledge the message.")

            return self.client.recv(1024).decode()
        except socket.error as e:
            if e.errno != 10038 and e.errno != 10054:
                print(f"Socket error: {e}")

            return None


    def client_version(self):
        try:
            time.sleep(buffer)
            self.client.send(bytes(f"6|", "utf-8"))

            acknowledgment = self.client.recv(1024).decode()
            if acknowledgment != "ACK":
                print("Error: Client did not acknowledge the message.")

            device = self.client.recv(1024).decode()
            return device
        except socket.error as e:
            if e.errno != 10038 and e.errno != 10054:
                print(f"Socket error: {e}")

            return None


    def weather(self):
        try:
            time.sleep(buffer)
            self.client.send(bytes(f"7|dummy", "utf-8"))

            acknowledgment = self.client.recv(1024).decode()
            if acknowledgment != "ACK":
                print("Error: Client did not acknowledge the message.")

        except socket.error as e:
            if e.errno != 10038 and e.errno != 10054:
                print(f"Socket error: {e}")


    def hidden_input(self, string):
        try:
            time.sleep(buffer)
            self.client.send(bytes(f"8|{string}", "utf-8"))

            acknowledgment = self.client.recv(1024).decode()
            if acknowledgment != "ACK":
                print("Error: Client did not acknowledge the message.")

            return self.client.recv(1024).decode()
        except socket.error as e:
            if e.errno != 10038 and e.errno != 10054:
                print(f"Socket error: {e}")

            return None


    def printc(self, string, color):
        colours = ["black", "red", "green", "yellow", "blue", "magenta", "cyan",
                   "light_red", "light_green", "light_yellow",
                   "light_blue", "light_magenta", "light_cyan", "white"]  # compatible colours

        try:
            time.sleep(buffer)
            if len(color) == 1:
                color.append("black")
            if color[0] in colours:
                if color[1] in colours:
                    self.client.send(bytes(f"9|{json.dumps(color)}|{string}", "utf-8"))

            else:
                print("Error: Invalid colour")
                self.client.send(bytes(f"9|{['white']}|{string}", "utf-8"))


            acknowledgment = self.client.recv(1024).decode()
            if acknowledgment != "ACK":
                print("Error: Client did not acknowledge the message.")

        except socket.error as e:
            if e.errno != 10038 and e.errno != 10054:
                print(f"Socket error: {e}")


    def print2d(self, array):


        try:
            time.sleep(buffer)

            self.client.send(bytes(f"10|{json.dumps(array)}", "utf-8"))

            acknowledgment = self.client.recv(1024).decode()
            if acknowledgment != "ACK":
                print("Error: Client did not acknowledge the message.")

        except socket.error as e:
            if e.errno != 10038 and e.errno != 10054:
                print(f"Socket error: {e}")


    def print2dc(self, array):
        try:
            time.sleep(buffer)
            self.client.send(bytes(f"11|{json.dumps(array)}", "utf-8"))
            acknowledgment = self.client.recv(1024).decode()
            if acknowledgment != "ACK":
                print("Error: Client did not acknowledge the message.")

        except socket.error as e:
            if e.errno != 10038 and e.errno != 10054:
                print(f"Socket error: {e}")


    def set_mode(self, mode):
        try:
            time.sleep(buffer)
            self.client.send(bytes(f"12|{mode}", "utf-8"))
            acknowledgment = self.client.recv(1024).decode()
            if acknowledgment != "ACK":
                print("Error: Client did not acknowledge the message.")

        except socket.error as e:
            if e.errno != 10038 and e.errno != 10054:
                print(f"Socket error: {e}")


    def get_key_state(self, key):
        try:
            time.sleep(buffer)
            self.client.send(bytes(f"13|{key}", "utf-8"))



            acknowledgment = self.client.recv(1024).decode()

            key = self.client.recv(1024).decode()
            if acknowledgment != "ACK":
                print("Error: Client did not acknowledge the message.")

            return key
        except socket.error as e:
            if e.errno != 10038 and e.errno != 10054:
                print(f"Socket error: {e}")

            return None

    def device(self):
        try:
            time.sleep(buffer)
            self.client.send(bytes(f"14|", "utf-8"))

            acknowledgment = self.client.recv(1024).decode()
            if acknowledgment != "ACK":
                print("Error: Client did not acknowledge the message.")

            device = self.client.recv(1024).decode()
            return device
        except socket.error as e:
            if e.errno != 10038 and e.errno != 10054:
                print(f"Socket error: {e}")

            return None

    def closet(self, string):
        try:
            time.sleep(buffer)
            self.client.send(bytes(f"15|{string}", "utf-8"))

            acknowledgment = self.client.recv(1024).decode()
            if acknowledgment != "ACK":
                print("Error: Client did not acknowledge the message.")

            self.client.close()
            print(f"{self.client_ip} has disconnected from the server at {datetime.datetime.now()}")
        except socket.error as e:
            if e.errno != 10038 and e.errno != 10054:
                print(f"Socket error: {e}")





