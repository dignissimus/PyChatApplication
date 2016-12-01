from easygui import *
import socket
import threading
import tkinter
from tkinter import ttk
details = multenterbox("Server Details", "Chat Client", ["IP", "Port", "Name(optional)"])
ip = details[0]
port = details[1]
name = details[2]

if name.split(" ")[0] != "":
    name = name.split(" ")[0]


def receive(client):
    global chatlog
    while True:
        data = client.recv(1024)
        data=data.decode("utf-8")
        chatlog.config(state=tkinter.NORMAL)
        chatlog.insert(tkinter.END, data + "\n")
        chatlog.config(state=tkinter.DISABLED)


def send(sender):
    tosend = chat.get()
    sender.sendall(bytes(tosend, "utf-8"))


def main():
    global ip
    global port
    global name
    global connect
    print("main")
    connect = socket.socket()
    connect.connect((ip, int(port)))
    t = threading.Thread(target=receive, args=[connect])
    t.start()
    # I don't need to send at the same time.
    # t = threading.Thread(target=send, args=connect)
    # t.start()
    # THE ACTUAL CHATTER


client = tkinter.Tk()
chatlog = tkinter.Text(client)
chatlog.insert(tkinter.END, "The Chatlog...\n")
chatlog.config(state=tkinter.DISABLED)
chatlog.pack()
chat = tkinter.Entry(client)
chat.pack()
sendoff = tkinter.Button(client, text="Send", command=lambda:send(connect))
sendoff.pack()
t = threading.Thread(target=main)
t.start()
client.mainloop()
