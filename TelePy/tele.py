import socket
import threading
import json
import time
import datetime
import logging
import signal
import sys

buffer = 0

settings = {}

active_terminal_clients = set()
active_terminal_clients_lock = threading.Lock()

start_time = None
shutdown_requested = False

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def signal_handler(signum, frame):
    global shutdown_requested
    logger.info("Signal received, initiating shutdown...")
    shutdown_requested = True
    sys.exit(0)

signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

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

        
        "light_black": "\033[1;30m",
        "light_red": "\033[1;31m",
        "light_green": "\033[1;32m",
        "light_yellow": "\033[1;33m",
        "light_blue": "\033[1;34m",
        "light_magenta": "\033[1;35m",
        "light_cyan": "\033[1;36m",
        "light_white": "\033[1;37m",

        "reset": "\033[0m"
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
        "light_black": "\033[1;40m",
        "light_red": "\033[1;41m",
        "light_green": "\033[1;42m",
        "light_yellow": "\033[1;43m",
        "light_blue": "\033[1;44m",
        "light_magenta": "\033[45m",
        "light_cyan": "\033[1;46m",
        "light_white": "\033[1;47m",
        'reset': '\033[0m'
    }

    color_code = colors.get(color, colors['reset'])
    background_code = backgrounds.get(background, '')

    return f"{background_code}{color_code}{text}{colors['reset']}"

def load_config():
    global settings
    with open('config.json', "r") as f:
       settings = json.load(f)

def load_json(name):
    global settings
    with open(f'{name}.json', "r") as f:
        return json.load(f)       

def test():
    print(f"You are using telepy!")


def log(filename, text):
    print(text)
    with open(filename, 'a') as file:
        file.write(text + '\n')


def setup(port):
    global settings
    Sct = socket.socket()  # creating the socket
    
    Sct.bind(("", int(port)))  # Bind port
    Sct.listen(5)  # listens for clients
    print(f'Telepy server started on port:{port}')
    return Sct


def setup_log(port, log_file):
    global settings
    Sct = socket.socket()  # creating the socket
    
    Sct.bind(("", int(port)))  # Bind port
    Sct.listen(5)  # listens for clients
    log(log_file, f'Tele py server started on port:{port}!')
    return Sct

def start_uptime():
    global start_time
    start_time = time.time()

def get_uptime():
    global start_time
    if start_time is None:
        return "Uptime not started."
    elapsed_time = time.time() - start_time
    hours, remainder = divmod(int(elapsed_time), 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours}h {minutes}m {seconds}s"


        

def handle_client_connection_wrapper(client_side, client):
    try:
        logger.info(f"Handling client {client.client_ip}")
        client_side(client)
    except Exception as e:
        logger.error(f"Error handling client {client.client_ip}: {e}")
    finally:
        with active_terminal_clients_lock:
            active_terminal_clients.discard(threading.current_thread())
            active_count = len({t for t in active_terminal_clients if t.is_alive()})
        logger.info(f"Client {client.client_ip} disconnected. Active: {active_count}")
        try:
            client.client.close()
        except:
            pass

def handle_ping_connection_wrapper(client_socket):
    try:
        client_socket.send(b"pong")
    finally:
        try:
            client_socket.close()
        except:
            pass

def handle_json_connection_wrapper(client_socket):
    try:
        server_config = load_json('info')
        with active_terminal_clients_lock:
            active_count = len({t for t in active_terminal_clients if t.is_alive()})
        server_info = {
            'name': server_config['server_name'],
            'description': server_config['description'],
            'icon': server_config['icon'],
            'uptime': get_uptime(),
            'online': active_count
        }
        client_socket.send(bytes(json.dumps(server_info), "utf-8"))
    except Exception as e:
        logger.error(f"JSON request failed: {e}")
    finally:
        try:
            client_socket.close()
        except:
            pass

def start_telepy(client_side, port):
    load_config()
    start_uptime()
    
    sct = setup(port)
    
    while True:
        if shutdown_requested:
            break
            
        try:
            client_socket, client_address = sct.accept()
            client_socket.settimeout(25)
            
            try:
                connection_type = client_socket.recv(1024).decode().strip()
            except socket.timeout:
                logger.warning(f"Timeout from {client_address}")
                client_socket.close()
                continue

            if connection_type == 'terminal':
                with active_terminal_clients_lock:
                    active_count = len({t for t in active_terminal_clients if t.is_alive()})
                
                max_conn = settings.get('max_connections', 50)
                if active_count >= max_conn:
                    logger.warning(f"Connection limit reached, rejecting {client_address}")
                    try:
                        client_socket.send(b"REJECTED|max_connections\n")
                    except:
                        pass
                    client_socket.close()
                    continue
                
                client_obj = Client(client_socket, client_address)
                client_thread = threading.Thread(
                    target=handle_client_connection_wrapper,
                    args=(client_side, client_obj),
                    name=f"TerminalClient-{client_address}"
                )
                client_thread.start()
                
                with active_terminal_clients_lock:
                    active_terminal_clients.add(client_thread)
                
                logger.info(f"Client connected. Active: {active_count + 1}")

            elif connection_type == 'ping':

                ping_thread = threading.Thread(
                    target=handle_ping_connection_wrapper,
                    args=(client_socket, ),
                    name=f"Ping-{client_address}"
                )
                ping_thread.start()

            elif connection_type == 'json':

                ping_thread = threading.Thread(
                    target=handle_json_connection_wrapper,
                    args=(client_socket, ),
                    name=f"Json-{client_address}"
                )
                ping_thread.start()

            else:
                logger.warning(f"Unknown connection type '{connection_type}' from {client_address}")
                client_socket.close()

        except Exception as e:
            logger.error(f"Fatal error: {e}")


class Client:

    def __init__(self, client_id, client_ip):
        self.client = client_id
        self.client_ip = client_ip

    def _recv_data(self):
        response = self.client.recv(1024).decode().strip()
        if response == "ACK":
            return self.client.recv(1024).decode()
        if response.startswith("ACK"):
            return response[3:].strip()
        return response

    def print(self, string):
        try:
            to_send = string.split('\n')
            for string in to_send:
                string = string.replace('|', '($SEP$)')
                self.client.send(bytes(f"0|{string}\n", "utf-8"))

                ack = self.client.recv(1024).decode()
                ack = ack.replace('\n', '')
                if ack != "ACK":
                    print("Error: Client did not acknowledge the message.")


        except socket.error as e:
            if e.errno != 10038 and e.errno != 10054:
                print(f"Socket error: {e}")


    def input(self, string):
        try:
            string = string.replace('|', '($SEP$)')
            self.client.send(bytes(f"1|{string}\n", "utf-8"))
            return self._recv_data()
        except socket.error as e:
            if e.errno != 10038 and e.errno != 10054:
                logger.error(f"Socket error in input: {e}")
            return None


    def close(self, string):
        try:
            string = string.replace('|', '($SEP$)')
            self.client.send(bytes(f"2|{string}\n", "utf-8"))

            ack = self.client.recv(1024).decode()
            ack = ack.replace('\n', '')
            if ack != "ACK":
                print("Error: Client did not acknowledge the message.")

            self.client.close()
            
        except socket.error as e:
            if e.errno != 10038 and e.errno != 10054:
                print(f"Socket error: {e}")


    def cls(self):
        try:
            time.sleep(buffer)
            self.client.send(bytes(f"3|\n", "utf-8"))

            ack = self.client.recv(1024).decode()
            ack = ack.replace('\n', '')
            if ack != "ACK":
                print("Error: Client did not acknowledge the message.")

        except socket.error as e:

            if e.errno != 10038 and e.errno != 10054:
                print(f"Socket error: {e}")


    def blankline(self):
        try:
            time.sleep(buffer)
            self.client.send(bytes(f"4|\n", "utf-8"))

            ack = self.client.recv(1024).decode()
            ack = ack.replace('\n', '')
            if ack != "ACK":
                print("Error: Client did not acknowledge the message.")

        except socket.error as e:
            if e.errno != 10038 and e.errno != 10054:
                print(f"Socket error: {e}")


    def password(self, string):
        try:
            string = string.replace('|', '($SEP$)')
            self.client.send(bytes(f"5|{string}\n", "utf-8"))
            return self._recv_data()
        except socket.error as e:
            if e.errno != 10038 and e.errno != 10054:
                logger.error(f"Socket error in password: {e}")
            return None


    def client_version(self):
        try:
            self.client.send(bytes(f"6|\n", "utf-8"))
            return self._recv_data()
        except socket.error as e:
            if e.errno != 10038 and e.errno != 10054:
                logger.error(f"Socket error in client_version: {e}")
            return None


    def weather(self):
        try:
            time.sleep(buffer)
            self.client.send(bytes(f"7|dummy\n", "utf-8"))

            ack = self.client.recv(1024).decode()
            ack = ack.replace('\n', '')
            if ack != "ACK":
                print("Error: Client did not acknowledge the message.")

        except socket.error as e:
            if e.errno != 10038 and e.errno != 10054:
                print(f"Socket error: {e}")


    def hidden_input(self, string):
        try:
            string = string.replace('|', '($SEP$)')
            self.client.send(bytes(f"8|{string}\n", "utf-8"))
            return self._recv_data()
        except socket.error as e:
            if e.errno != 10038 and e.errno != 10054:
                logger.error(f"Socket error in hidden_input: {e}")
            return None


    def printc(self, string, color):
        colours = ["black", "red", "green", "yellow", "blue", "magenta", "cyan",
                   "light_red", "light_green", "light_yellow",
                   "light_blue", "light_magenta", "light_cyan", "white"]  # compatible colours

        try:
            string = string.replace('|', '($SEP$)')
            if len(color) == 1:
                color.append("black")
            if color[0] in colours:
                if color[1] in colours:
                    self.client.send(bytes(f"9|{json.dumps(color)}|{string}\n", "utf-8"))

            else:
                print("Error: Invalid colour")
                self.client.send(bytes(f"9|{['white']}|{string}\n", "utf-8"))


            ack = self.client.recv(1024).decode()
            ack = ack.replace('\n', '')
            if ack != "ACK":
                print("Error: Client did not acknowledge the message.")

        except socket.error as e:
            if e.errno != 10038 and e.errno != 10054:
                print(f"Socket error: {e}")


    def print2d(self, array):


        try:
            string = json.dumps(array)

            string = string.replace('|', '($SEP$)') 

            self.client.send(bytes(f"10|{string}\n", "utf-8"))

            ack = self.client.recv(1024).decode()
            ack = ack.replace('\n', '')
            if ack != "ACK":
                print("Error: Client did not acknowledge the message.")

        except socket.error as e:
            if e.errno != 10038 and e.errno != 10054:
                print(f"Socket error: {e}")


    def print2dc(self, screen):
        try:
            
            
            for row in screen:
                for item in row:
                    char, fg_color, bg_color = item
                    # Print the character with the specified foreground and background colors
                    self.line(colour(char, fg_color, bg_color))
                self.print(" ")  # Move to the next line after printing each row
            return None
            

        except socket.error as e:
            if e.errno != 10038 and e.errno != 10054:
                print(f"Socket error: {e}")


    def set_mode(self, mode):
        try:
            time.sleep(buffer)
            self.client.send(bytes(f"12|{mode}\n", "utf-8"))
            ack = self.client.recv(1024).decode()
            ack = ack.replace('\n', '')
            if ack != "ACK":
                print("Error: Client did not acknowledge the message.")

        except socket.error as e:
            if e.errno != 10038 and e.errno != 10054:
                print(f"Socket error: {e}")


    def get_key_state(self, key):
        try:
            self.client.send(bytes(f"13|{key}\n", "utf-8"))
            return self._recv_data()
        except socket.error as e:
            if e.errno != 10038 and e.errno != 10054:
                logger.error(f"Socket error in get_key_state: {e}")
            return None

    def device(self):
        try:
            self.client.send(bytes(f"14|\n", "utf-8"))
            return self._recv_data()
        except socket.error as e:
            if e.errno != 10038 and e.errno != 10054:
                logger.error(f"Socket error in device: {e}")
            return None
        
    def switch(self, string):
        try:
            string = string.replace('|', '($SEP$)')
            self.client.send(bytes(f"15|{string}\n", "utf-8"))
            status = self._recv_data()

            if status == 'switch':
                self.client.close()
                logger.info(f"{self.client_ip} switched to {string}")
                return True
            else:
                return False
        except socket.error as e:
            if e.errno != 10038 and e.errno != 10054:
                logger.error(f"Socket error in switch: {e}")
            return None
        
    def line(self, string):
        try:
            to_send = string.split('\n')
            for string in to_send:
                string = string.replace('|', '($SEP$)')
                self.client.send(bytes(f"19|{string}\n", "utf-8"))

                ack = self.client.recv(1024).decode()
                ack = ack.replace('\n', '')
                if ack != "ACK":
                    print("Error: Client did not acknowledge the message.")


        except socket.error as e:
            if e.errno != 10038 and e.errno != 10054:
                print(f"Socket error: {e}")

    def get_ip(self): # Mode 16
        return self.client_ip[0]
    
    
