import sys
import socket
import datetime
import time
import json
import threading
import signal 
import logging
import atexit
from . import ssh as sshmod
from . import tele as tele
from . import telnet as telenet
buffer = 0

settings = {}

active_terminal_clients = set()
active_terminal_clients_lock = threading.Lock()

__version__ = "0.1.0"
start_time = None
shutdown_requested = False
server_threads = []

MAX_CONNECTIONS = 50

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('server.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def cleanup_dead_threads():
    global active_terminal_clients
    while not shutdown_requested:
        time.sleep(5)
        with active_terminal_clients_lock:
            dead = {t for t in active_terminal_clients if not t.is_alive()}
            for t in dead:
                active_terminal_clients.discard(t)
            if dead:
                logger.info(f"Cleaned up {len(dead)} dead threads. Active: {len(active_terminal_clients)}")

def get_active_count():
    with active_terminal_clients_lock:
        return len({t for t in active_terminal_clients if t.is_alive()})

def shutdown(signum, frame): 
    global shutdown_requested
    logger.info("Shutdown signal received, stopping gracefully...")
    shutdown_requested = True
    for t in server_threads:
        if t.is_alive():
            t.join(timeout=2)
    logger.info("All server threads stopped.")
    sys.exit(0)

def register_server_thread(thread):
    server_threads.append(thread)

def load_config():
    global settings, MAX_CONNECTIONS
    with open('config.json', "r") as f:
       settings = json.load(f)
    MAX_CONNECTIONS = settings.get('max_connections', 50)

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
        Sct.settimeout(5)
        Sct.connect((server_ip, port))
        Sct.send(b'json')
        server_json = Sct.recv(6000).decode()
        Sct.close()
        return json.loads(server_json)
    except Exception as e:
        logger.error(f"Failed to get server info: {e}")
        return False

def ping(server_ip):
    server = server_ip.split(':')
    port = 1998
    if len(server) == 2:
        server_ip = server[0]
        port = int(server[1])
    try:
        Sct = socket.socket()
        Sct.settimeout(5)
        start_time = time.time()
        Sct.connect((server_ip, port))
        Sct.send(b'ping')
        response = Sct.recv(1024).decode()
        Sct.close()
        if response.strip().lower() == "pong":
            return (time.time() - start_time) * 1000
        return False
    except Exception as e:
        logger.error(f"Ping failed: {e}")
        return False 

def date():
    return datetime.datetime.now().date()

def start(client_side):
    global shutdown_requested
    signal.signal(signal.SIGTERM, shutdown) 
    signal.signal(signal.SIGINT, shutdown)
    atexit.register(lambda: logger.info("Process exiting"))
    load_config()
    logger.info(f"Starting server with max_connections={MAX_CONNECTIONS}")
    
    cleanup_thread = threading.Thread(target=cleanup_dead_threads, daemon=True)
    cleanup_thread.start()
    
    for type in settings.keys():
        if type in ('telepy', 'ssh', 'telnet') and settings[type].get('enabled'):
            try:
                if type == 'telepy':
                    server_thread = threading.Thread(
                        target=tele.start_telepy,
                        args=(client_side, settings[type]['port']),
                        name=f"ServerThread-{type}",
                        daemon=True
                    )
                elif type == 'ssh':
                    server_thread = threading.Thread(
                        target=sshmod.start_ssh,
                        args=(client_side, settings[type]['port']),
                        name=f"ServerThread-{type}",
                        daemon=True
                    )
                elif type == 'telnet':
                    server_thread = threading.Thread(
                        target=telenet.start_bbs_server,
                        args=(client_side, settings[type]['port']),
                        name=f"ServerThread-{type}",
                        daemon=True
                    )
                server_thread.start()
                register_server_thread(server_thread)
                logger.info(f"Started {type} server on port {settings[type]['port']}")
            except Exception as e:
                logger.error(f'Failed to start {type} server: {e}')

    try:
        while not shutdown_requested:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received")
        shutdown(None, None)



