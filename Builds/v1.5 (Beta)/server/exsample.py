from TelePy import tp as tp
import threading  # This is use for multiple clients


def clientside(client):  # Function contain the client code just parse the client object

    client.print("Hello world!")
    client.input("Press Enter to continue...")  # This returns a value this is not used in this case
    client.closet(f"Disconnected by Server!")  # Disconnects the user


Sct = tp.setup()  # Creates a socket

while True:
    client_c, add = Sct.accept()
    print(f"{add} has connected to server.")
    client = tp.Client(client_c, add)
    threading._start_new_thread(clientside, (client,))
