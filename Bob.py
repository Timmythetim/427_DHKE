import pyDH
import socket
import threading
import sys

HOST = "127.0.0.1" 
PORT = 45001
SERVERPORT = 45000

def ListeningLoop(s):
    message = s.recv(1024)
    print(message)
    pass


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.connect((HOST,SERVERPORT))
    # x = threading.Thread(target=ListeningLoop, args=(s,))
    # x.start()
    while(1):
        a = input()
        s.send(bytes(a,"utf-8"))
        if a == "quit":
            s.close()
            break