import multiprocessing
import threading
import socket
import interpreter
import configparser
import os
import sys

if os.path.isfile("./settings.ini"):
    cp = configparser.ConfigParser()
    cp.read("./settings.ini")
    config = cp["settings"]
    port = config["port"]
    usemax = config.getboolean("usemax")
    if usemax:
        maxcon = config.getint("maxconnections")
    serverfull = config["server_full_message"]
    defload = config.getboolean("defaultloader")
    extload = config.get("loader")
else:
    print("ERROR: CONFIG FILE NOT FOUND")
    input()
    sys.exit()
# Copyright  2016, Sam Enwere-Ezeh, All rights reserved

__author__ = "Sam Enwere-Ezeh"
__copyright__ = "Copyright 2016-2017, United Kingdom, All rights reserved"
# T#O#D#O create a config file to edit settings #DONE
server = socket.socket()
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # stack overflow answer: force port open
server.bind(('', int(port)))
server.listen(5)  # max connections
number = 0
clients = {}
names = {}
blocklist = []


def command(text, user):
    user = user
    origcmd = text
    text = text.lower()
    action = text.replace("(command)", "")
    execute = interpreter.interpret(action)
    execute = execute.replace("$INSERTVALUEHERE", "user")
    try:
        exec(execute)
        # print(execute) for debugging only
    except:
        exec('print(\"Malformed Request from: \"+user[0]+\" reads:\")')
        print(origcmd)
        # print("was going to run:\n" + execute) for debugging only


def handle(connection, address):
    # print(address, connection) # Used For Debugging
    global clients
    global names
    if address not in clients:
        clients[address] = connection
        names[address] = address[0]
    if address not in names:
        names[address] = address[0]
    # print(clients) for debugging only
    while True:
        try:  # if connection is not broken
            receive = connection.recv(1024).decode("utf-8")
        except:  # if it is
            try:
                del clients[address]  # disconnect from client
                sys.exit()
            except:
                sys.exit()
                pass
                # something broke so leave it
        if receive.lower().startswith("(command)"):
            command(receive.lower(), address)
        else:
            sendto = clients  # I did this because i got an error as the dictionary changed
            for key in sendto:
                try:
                    sendto[key].sendall(bytes(names[address] + " Wrote: " + receive + "\n", "utf-8"))
                    # print("sent") for debugging only
                except:  # if connection is broken
                    try:
                        del clients[key]  # remove client from list   (A GHOST IS AMONG US)
                        sys.exit() #
                    except:
                        sys.exit()
                        pass  # Client


def loader():  # to add support for external loaders
    global connector
    global blocklist
    if connector[1][0] in blocklist:
        connector[0].sendall(b"you are Blocked ;)\n")
        connector[0].close()
        pass
    if not usemax or len(clients) < maxcon:
        t = threading.Thread(target=handle, args=connector)
        t.start()
        # had to use threads as (An Answer on StackOverflow showed that) processes have separate memory stores
    else:
        try:
            connector[0].sendall(bytes(serverfull, "utf-8"))
            connector[0].close()
        except:
            connector.close()
            pass  # IT DOESNT MATTER WHAT YOUR IP IS (the rock)


if not defload:
    loaderdir = os.path.abspath("./plugins/loaders/") + "/"
    file = open(loaderdir + extload)
    torun = file.read()
    file.close()
    exec(torun)
else:
    pass  # using default loader


def broadcast(message):
    global clients
    for client in clients:
        clients[client].sendall(message)


def start():
    global connector
    global server
    while True:
        connector = server.accept()
        loader()


if __name__ == '__main__':
    while True:
        connector = server.accept()
        loader()
