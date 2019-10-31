#!/usr/bin/env python3
"""Script for Tinker GUI chat client."""

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter

def receive():
    """Handles receiving of messages."""
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(tkinter.END, msg)
        except OSError: # Possibly client has left the chat.
            break

def send(event=None):   # event is passed by binders.
    """Handles sending of messages."""
    msg = my_msg.get()
    my_msg.set("")  # Clears input field.
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{exit}":
        client_socket.close()
        top.quit()

def on_closing(event=None):
    """This function is to be called when the window is closed."""
    my_msg.set("User has left the chat room unexpectedly")
    send()
    client_socket.close()
    top.quit()

top = tkinter.Tk()
top.title("simpleChat")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()    # For the messages to be sent.
my_msg.set("Type your message here.")
scrollbar = tkinter.Scrollbar(messages_frame)   # To navigate through past messages.

msg_list = tkinter.Listbox(messages_frame, height=20, width=75, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()

messages_frame.pack()

def clear_text(event):
    entry_field.delete(0, tkinter.END)

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.bind("<Button-1>", clear_text)
entry_field.bind("<FocusIn>", clear_text)

entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)

HOST = input('Enter host: ')
PORT = input('Enter port: ')

if not PORT:
    PORT = 33000    # Default value.
else:
    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()  # Starts GUI execution.