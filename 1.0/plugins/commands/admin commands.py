import threading

password = "pass123"


def stop(code, index):
    print("sending the server to a HALT")
    import os
    os._exit(1)

def blockip(code, index):
    global loaded
    global blocklist
    ip=code[index+1]
    loaded="""\
global loaded
global blocklist
global clients
blocklist.append("{}")
for client in clients:
    if client[0]=='{}':
        clients[client].close()
        del clients[client]""".format(ip, ip)
    print(loaded)

def endit(seconds):
    import os, sys, time
    time.sleep(int(seconds))
    python = sys.executable
    os.execl(python, python, *sys.argv)


def restart(code, index):
    seconds = 5  # seconds
    import os
    import sys
    global loaded
    global broadcast
    # broadcast("[Server] Going for server RESTART")
    loaded = """\
for client in clients:
    try:
        clients[client].sendall(b"Going To Restart in """+str(seconds)+""" Seconds\\n")
    except:
        pass
    """
    t= threading.Thread(target=endit, args=[seconds])
    t.start()


def checkpass(pwd):
    return pwd == password


admincmds = {"stop": stop,
             "restart": restart,
             "blockip": blockip}


def admin(code, index):
    global password
    global admincmds
    try:
        inpass = code[index + 1]
    except:
        print("[ADMIN]Malformed Request")
    if inpass == password:
        try:
            command = code[index + 2]
        except:
            print("[ADMIN] Malformed request: " + command)
        if command in admincmds:
            admincmds[command](code, code.index(command))
        else:
            print("No command matching " + command)
    else:
        print("Wrong Password")


functions = {"admin": admin}
