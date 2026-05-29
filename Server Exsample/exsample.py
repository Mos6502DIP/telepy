import TelePy as tp
import os

os.chdir(os.path.dirname(os.path.abspath(__file__))) # Fixes issues related to files being incorrect

def client_side(client):  # Function contain the client code just parse the client object

    client.print("Hello world!")
    client.input("Press Enter to continue...")  # This returns a value this is not used in this case
    client.closet(f"Disconnected by Server!")  # Disconnects the user

if __name__ == '__main__':
    tp.start(client_side)  # Starts a server based on the config txt