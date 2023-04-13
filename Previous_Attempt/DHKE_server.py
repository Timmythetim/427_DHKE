import socket
import sys
import threading
import random
from Diffie_Hellman_Merkle import *
HOST = "127.0.0.1" 
PORT = 45000
sAlice = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sBob = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sAlice.bind((HOST, PORT))
sBob.bind((HOST, PORT-1))
alice = DiffieHellman()
bob = DiffieHellman()
alice.set_public_key()
bob.set_public_key()


print(alice.public_key)
class packet():
    def __init__(self):
        self.recipient = ""
        self.message = ""
        self.p = 0
        self.g = 0
    def convert_message_to_packet(self):
        packet = ""
        packet += self.recipient
        packet += "\0"
        packet += self.message
        return packet

def bytes_to_packet(bytestring):
    p1 = packet()
    counter = 0
    while bytestring[counter] != 0:
        p1.recipient += chr(bytestring[counter])
        counter += 1
    p1.message = bytestring[counter+1:]
    p1.message = p1.message.decode()
    return p1

# ALICEPORT = 45001
# BOBPORT = 45002
# EVEPORT = 45003

def ProcessingLoop(conn,addr, name):
    print("Connected to: ",addr)
    p1 = packet()
    global alice
    global bob
    a = conn.recv(1024)
    p1 = bytes_to_packet(a)
    if name == "Alice":
        if p1.message == "ALICE" and p1.recipient == "HANDSHAKE":
            a = conn.recv(1024)
            alice.public_key = int(str(a,"utf-8")) 
            print(alice.public_key)
            a = conn.recv(1024)
            p1 = bytes_to_packet(a)
            if p1.message == "Bob":
                conn.send(bob.public_key)
            while(1):
                a = conn.recv(1024)
                p1 = bytes_to_packet(a)
                if p1.recipient == "Bob":
                    sBob.send(p1.message.encode())
    if name == "Bob":
        if p1.message == "BOB" and p1.recipient == "HANDSHAKE":
            a = conn.recv(1024)
            bob.public_key = int(str(a,"utf-8"))
            print(bob.public_key)
            if p1.message == "Alice":
                conn.send(alice.public_key)
            while(1):
                a = conn.recv(1024)
                p1 = bytes_to_packet(a)
                if p1.recipient == "Alice":
                    sBob.send(p1.message.encode())



if __name__ == "__main__":
    sAlice.listen()
    conn, addr = sAlice.accept()
    print("Hello!")
    x = threading.Thread(target=ProcessingLoop, args=(conn, addr,"Alice",))
    x.start()
    sBob.listen()
    conn, addr = sBob.accept()
    print("Hello!")
    y = threading.Thread(target=ProcessingLoop, args=(conn, addr,"Bob",))
    y.start()

