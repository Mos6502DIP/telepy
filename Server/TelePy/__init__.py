import sys
import socket
import datetime
import time
import json
import time
import threading
import signal 
import sys
import TelePy.ssh as sshmod
import TelePy.tele as tele
import TelePy.telnet as telenet
buffer = 0

settings = {}

active_terminal_clients = set()
active_terminal_clients_lock = threading.Lock()

start_time = None

def shutdown(signum, frame): 
    print("Shutting down cleanly...") 
    sys.exit(0)

def load_config():
    global settings
    with open('config.json', "r") as f:
       settings = json.load(f)

def load_json(name):
    global settings
    with open(f'{name}.json', "r") as f:
        return json.load(f)       

def get_info(server_ip):
    try:
        server = server_ip.split(':')
        port = 1998
        if len(server) == 2:

            server_ip = server[0]

            port = int(server[1])

        Sct = socket.socket()
        Sct.connect((server_ip, port))
        Sct.send(bytes('json', "utf-8"))
        server_json = Sct.recv(6000).decode()
        Sct.close()
        return json.loads(server_json)
    
    except (socket.timeout, socket.error) as e:
        return False

def ping(server_ip):
    server = server_ip.split(':')
    port = 1998
    if len(server) == 2:

        server_ip = server[0]

        port = int(server[1])

    try:
        Sct = socket.socket()
        Sct.settimeout(5)  # Optional: timeout after a few seconds

        start_time = time.time()
        Sct.connect((server_ip, port))
        
        Sct.send(b'ping')  # Send "ping"
        
        response = Sct.recv(1024).decode()
        end_time = time.time()

        Sct.close()

        if response.strip().lower() == "pong":
            ping_ms = (end_time - start_time) * 1000  # Convert to milliseconds
            return ping_ms
        else:
            return False

    except (socket.timeout, socket.error) as e:
        return False 


def date():
    current_datetime = datetime.datetime.now()
    return current_datetime.date()

def start(client_side):
    signal.signal(signal.SIGTERM, shutdown) 
    signal.signal(signal.SIGINT, shutdown)
    load_config()
    for type in settings.keys():
        if settings[type]['enabled']:

            if type == 'telepy':
                server_thread = threading.Thread(
                    
                    target=tele.start_telepy,
                    args=(client_side, settings[type]['port']),
                    name=f"ServerThread-{type}",
                    daemon=True
                )
                server_thread.start()

            elif type == 'ssh':
                try:
                    
                    # Use the blocking start_ssh in its own thread
                    server_thread = threading.Thread(
                        target=sshmod.start_ssh,
                        args=(client_side, settings[type]['port']),
                        name=f"ServerThread-{type}",
                        daemon=True
                    )
                    server_thread.start()
                except Exception as e:
                    print(f'Failed to start ssh server: {e}')


            elif type == 'telnet':
                try:
                    
                    # Use the blocking start_ssh in its own thread
                    server_thread = threading.Thread(
                        target=telenet.start_bbs_server,
                        args=(client_side, settings[type]['port']),
                        name=f"ServerThread-{type}",
                        daemon=True
                    )
                    server_thread.start()
                except Exception as e:
                    print(f'Failed to start ssh server: {e}')

            else:
                print(f'Json syntax error Type:{type} is invalid.')

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping the threads Bye Bye :3")
        sys.exit(0)

