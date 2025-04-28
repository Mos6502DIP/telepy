import TelePy as tp


def client_side(client):  # Function contain the client code just parse the client object

    client.print("Hello world!")
    client.input("Press Enter to continue...")  # This returns a value this is not used in this case
    client.closet(f"Disconnected by Server!")  # Disconnects the user


tp.start(client_side)  # Starts a server based on the config txt