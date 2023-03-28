import socket
import threading
import sys
import time
from Diffie_Hellman_Merkle import *
HOST = "127.0.0.1" 
PORT = 45001
SERVERPORT = 45000
alice = DiffieHellman()
alice.set_public_key()

class packet():
    def __init__(self):
        self.recipient = ""
        self.message = ""
    def convert_message_to_packet(self):
        # plaintext = self.message 
        # self.message = ""
        packet = ""
        packet += self.recipient
        packet += "\0"
        # for c in plaintext:
        #     self.message+=chr(ord(c) + (alice.shared_key))
        packet += self.message
        return packet
    def convert_message_to_packet_encoded(self):
        plaintext = self.message 
        self.message = ""
        packet = ""
        packet += self.recipient
        packet += "\0"
        for c in plaintext:
            self.message+=chr(ord(c) + (alice.shared_key))
        packet += self.message
        return packet




def ListeningLoop(s):
    message = s.recv(1024)
    print(message)
    pass

if __name__ == "__main__":
    p1 = packet()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.connect((HOST,SERVERPORT))
        p1.message = "ALICE"
        p1.recipient = "HANDSHAKE"
        s.send(bytes(p1.convert_message_to_packet(),"utf-8"))
        time.sleep(.01)
        a = s.send(str(alice.public_key).encode())
        x = threading.Thread(target=ListeningLoop, args=(s,))
        while(1):
            if alice.shared_key == 0:
                a = input()
                p1.message = a
                p1.recipient = "Bob"
                s.send(bytes(p1.convert_message_to_packet(),"utf-8"))
                match p1.message:
                    case "quit":
                        s.close()
                        sys.exit()
                        break
                    case "Bob":
                        Bob_pubkey = int(s.recv(1024).decode())
                        alice.set_private_key(Bob_pubkey)
                        print(alice.shared_key)
            else:
                if not x.is_alive:
                    x.start()
                a = input()
                p1.message = a
                p1.recipient = "Bob"
                s.send(bytes(p1.convert_message_to_packet_encoded(),"utf-8"))
                match p1.message:
                    case "quit":
                        s.close()
                        sys.exit()
                        break

            
    