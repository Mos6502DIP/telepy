import os
import socket
import threading
import time
import json
import paramiko

HOST_KEY_PATH = os.path.join(os.path.dirname(__file__), "ssh_host.key")

version = 'SSH-1.9'

def colour(text, color, background=None, end='\n'):
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

    return f"{background_code}{color_code}{text}{colors['reset']}{end}"

def _get_config_ssh_password():
    """Return ssh password from Server/config.json if present, otherwise None."""
    cfg_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config.json'))
    try:
        with open(cfg_path, 'r') as f:
            cfg = json.load(f)
        ssh_conf = cfg.get('ssh', {})
        return ssh_conf.get('password')
    except Exception:
        return None


if paramiko is not None:
    class SimpleSSHServer(paramiko.ServerInterface):
        def __init__(self, allowed_password=None):
            self.event = threading.Event()
            self.allowed_password = allowed_password

        def check_channel_request(self, kind, chanid):
            if kind == "session":
                return paramiko.OPEN_SUCCEEDED
            return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

        def check_auth_password(self, username, password):
            # If no password configured, accept any password (backwards compatibility).
            if self.allowed_password is None:
                return paramiko.AUTH_SUCCESSFUL
            # Enforce exact match with configured password
            if password == self.allowed_password:
                return paramiko.AUTH_SUCCESSFUL
            return paramiko.AUTH_FAILED

        def check_channel_shell_request(self, channel):
            self.event.set()
            return True
else:
    SimpleSSHServer = None  # Paramiko missing, avoid attribute lookup errors at import time


class setup_connection:
    def __init__(self, chan, addr):
        self.chan = chan
        self.addr = addr
        self.message = ''
        self.auto_return = False

    def _recvline(self):
        buf = b""
        while True:
            data = self.chan.recv(1024)
            if not data:
                return None
            buf += data
            if b"\n" in buf or b"\r" in buf:
                break
        return buf.decode('utf-8').replace('\r', '').replace('\n', '').strip()

    def print(self, string):
        if '\n' in string or '\r\n' in string:
            lines = string.splitlines()
            for line in lines:
                self.chan.send((line + '\r\n').encode())
        else:
            self.chan.send((string + '\r\n').encode())

    def cls(self):
        # ANSI clear screen
        self.chan.send(b"\x1b[2J\x1b[H")

    def input(self, string):
        self.chan.send(string.encode())
        return self._recvline()

    def hidden_input(self, string):
        # No terminal echo control here; simply behave like normal input
        self.chan.send(string.encode())
        return self._recvline()
    
    def password(self, string):
        self.chan.send(string.encode())
        return self._recvline()

    def print_no_new_line(self, string):
        self.chan.send(string.encode())

    def blankline(self):
        self.chan.send(b"\r\n")

    def close(self, string=None):
        """Close the channel (optionally send a final message)."""
        try:
            if string:
                try:
                    self.print(string)
                except Exception:
                    pass
            self.chan.close()
        except Exception:
            pass

    def printc(self, string, data):
        
        self.chan.send(colour(string, data[0], data[1]))

    def print2d(self, data):
        self.chan.send('\n'.join([''.join(['{:4}'.format(item) for item in row])
                             for row in data]))
        self.chan.send('\n')
        
    def print2dc(self, data):
        for row in data:
            for item in row:
                char, fg_color, bg_color = item
                # Print the character with the specified foreground and background colors
                self.chan.send(colour(char, fg_color, bg_color, end=''))
            self.chan.send('\n')  # Move to the next line after printing each row

    def get_ip(self):
        return self.addr
    
    def switch(self, data):
        self.chan.send(f'Server attempted to switch to ({data}). Unable to due to ssh Client\n')
        


    def closet_log(self, log_file, string):
        """Send a goodbye message, close channel, and append a log line to `log_file`."""
        try:
            string = string or ''
            try:
                # Send the string before closing
                self.print(string)
            except Exception:
                pass
            self.chan.close()
            # Append to log file
            with open(log_file, 'a') as f:
                f.write(f"{self.addr} has disconnected from the server at {time.ctime()}: {string}\n")
        except Exception:
            pass

    

    def client_version(self):
        return version


def _ensure_host_key():
    # Generate a host key if not present
    if not os.path.exists(HOST_KEY_PATH):
        if paramiko is None:
            return None
        key = paramiko.RSAKey.generate(2048)
        key.write_private_key_file(HOST_KEY_PATH)
    return paramiko.RSAKey(filename=HOST_KEY_PATH)


def start_ssh(client_side, port):
    if paramiko is None:
        print("Paramiko is not installed. Install with: pip install paramiko")
        return

    _ssh_password = _get_config_ssh_password()
    if _ssh_password is None:
        print("Warning: no SSH password set in config.json — accepting any password.")
    else:
        print("SSH password loaded from config.json.")

    host_key = _ensure_host_key()
    if host_key is None:
        print("Unable to initialize SSH host key.")
        return

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("", int(port)))
    server_socket.listen(100)
    print(f"SSH Server running on port:{port}")

    def client_thread(client_socket, client_addr):
        try:
            transport = paramiko.Transport(client_socket)
            transport.add_server_key(host_key)
            server = SimpleSSHServer(allowed_password=_ssh_password)
            try:
                transport.start_server(server=server)
            except Exception as e:
                print(f"SSH negotiation failed: {e}")
                transport.close()
                return

            # Wait for a channel
            chan = transport.accept(25)
            if chan is None:
                transport.close()
                return

            # Wrap channel in setup_connection and call client_side handler
            conn = setup_connection(chan, client_addr)
            try:
                client_side(conn)
            except Exception as e:
                print(f"Error in client handler: {e}")
            finally:
                try:
                    chan.close()
                except Exception:
                    pass
                transport.close()
        except Exception as e:
            print(f"SSH client exception: {e}")
            try:
                client_socket.close()
            except Exception:
                pass

    # Main accept loop
    while True:
        time.sleep(0.001)
        print('Waiting for next SSH connection')
        client_socket, client_addr = server_socket.accept()
        print(f"SSH connection from {client_addr}")
        t = threading.Thread(target=client_thread, args=(client_socket, client_addr), name=f"SSHClient-{client_addr}")
        t.daemon = True
        t.start()


# Simple helper to start server in background thread (used by __init__.py start())
def start_ssh_background(client_side, port, log_file):
    t = threading.Thread(target=start_ssh, args=(client_side, port, log_file), name=f"ServerThread-ssh")
    t.daemon = True
    t.start()
    return t
