from TelePy import tp as tp
import threading


def clientside(client, add):
    tp.printt("Hello world", client)
    user_input = tp.inputt("Enter some text :>", client)
    tp.printt(f"Hello, {user_input} thankyou for using telepy!", client)
    tp.closet(f"Server is now disconcerting!", client)



Sct = tp.setup("Pick a port number (98):> ", 120)

while True:
    client,add = Sct.accept()
    print("User has connected to server")
    threading._start_new_thread(clientside, (client, add))