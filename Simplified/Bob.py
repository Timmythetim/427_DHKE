import socket
import threading
from Diffie_Hellman_Merkle import *
HOST = "127.0.0.1" 
bob = DiffieHellman()
bob.set_public_key()

def ListeningLoop(conn):
    buffer = ""
    p = Packet()
    buffer = conn.recv(1024)
    buffer = buffer.decode("utf-8")
    buffer = int(buffer)
    bob.set_private_key(buffer)
    print(bob.shared_key,end = "\n\n")
    while True:
        p.iv_bytes = conn.recv(16)
        p.encrypted_message = conn.recv(1024)
        p.string_message = bob.decrypt_message(p.encrypted_message, p.iv_bytes)
        print()
        print("From: Alice - ", end = " ")
        print(p.string_message)
        
        
        
if __name__ == "__main__":
    mode = ""
    while (mode != "Y" and mode != "N"):
        mode = input("Would you like to run in evesdropping mode? (Y/N)")
    if mode == "N":
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sendport:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as receiveport:
                sendport.setblocking(1)
                receiveport.setblocking(1)
                receiveport.bind((HOST,BOBLISTEN))
                receiveport.listen()
                conn, addr = receiveport.accept()
                
                sendport.bind((HOST, BOBSEND))
                sendport.connect((HOST,ALICELISTEN))
                
                
                x = threading.Thread(target=ListeningLoop, args=(conn,))
                x.start()
                
                sendport.send(str(bob.public_key).encode("utf-8"))
                while True:
                    a = input("Bob:")
                    p = bob.encrypt_message(a)
                    sendport.send(p.iv_bytes)
                    sendport.send(p.encrypted_message)
                    print(p.encrypted_message)
    else:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sendport:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as receiveport:
                sendport.setblocking(1)
                receiveport.setblocking(1)
                
                sendport.bind((HOST, BOBSEND))
                sendport.connect((HOST,BOBtoEVEPORT))
                
                receiveport.bind((HOST,BOBLISTEN))
                receiveport.listen()
                conn, addr = receiveport.accept()
                
                x = threading.Thread(target=ListeningLoop, args=(conn,))
                x.start()               
                sendport.send(str(bob.public_key).encode("utf-8"))
                while True:
                    a = input("Bob:")
                    p = bob.encrypt_message(a)
                    sendport.send(p.iv_bytes)
                    sendport.send(p.encrypted_message)
                    print(p.encrypted_message)