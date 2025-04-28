from Server import TelePy as TelePy
import threading  # This is use for multiple clients


def clientside(client):  # Function contain the client code just parse the client object

    client.print("Ping")
    client.input("Press Enter to continue...")  # This returns a value this is not used in this case
    client.switch('@')  # Disconnects the user


Sct = TelePy.setup()  # Creates a socket

while True:
    client_c, add = Sct.accept()
    print(f"{add} has connected to server.")
    client = TelePy.Client(client_c, add)
    threading._start_new_thread(clientside, (client,))
