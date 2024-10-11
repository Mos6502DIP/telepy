# Telepy
 Telepy is a recreation of a teletype terminal interface using TCP this project has been going on for almost 3 years. It features encrypted inputs, colour text, colour 2d arrays and more. The project features a complied exe client, a version for Linux, and server tools. If  you want a server, try going to 'server.fractaldev.co' where Telepy-connect is running. This is also a project running alongside this not the only use for this project you can use it for server monitoring, making an online version of the cli python project and more. 
 

## Contents


# Client
## setup
To set up the client to download the latest release this should be in the format of `v(version).zip`. This file contains two folders a server folder and a client folder this folder will contain a and exe, py and txt files. If you are on Windows you can just run the exe (Windows Defender will pop up click more info then run anyway. If you do not feel that you can trust the exe run the Client.py in the source code this is not the most optimised version though and may not be the correct version.) if you are on a Linux distro run `Telepi.py`.

## Connecting to a server

To connect the server just enter the ip or the domain by default servers rn on port 1998. For the custom ports add `:` at the end of the IP/domain then the port eg `exsample.com:1234`. For the local host just enter `@` and `:` for the port eg `@:1234`.

## Config

As previously mentioned there is a file called `config.txt` that will contain the configuration for the client. They are currently in the format of `setting=option` with `#` being used for comments.
