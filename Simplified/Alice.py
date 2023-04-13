import socket
import threading
from Diffie_Hellman_Merkle import *
HOST = "127.0.0.1" 
alice = DiffieHellman()
alice.set_public_key()

def ListeningLoop(conn):
    p = Packet()
    buffer = conn.recv(1024)
    buffer = int(buffer.decode("utf-8"))
    alice.set_private_key(buffer)
    print(alice.shared_key)
    while True:
        p.iv_bytes = conn.recv(16)
        p.encrypted_message = conn.recv(1024)
        p.string_message = alice.decrypt_message(p.encrypted_message, p.iv_bytes)
        print()
        print("From: Bob - ", end = " ")
        print(p.string_message)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sendport:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as receiveport:
        sendport.setblocking(1)
        receiveport.setblocking(1)
        sendport.bind((HOST, ALICESEND))
        sendport.connect((HOST,BOBLISTEN))
        buffer = ""
        
        receiveport.bind((HOST,ALICELISTEN))
        receiveport.listen()
        conn, addr = receiveport.accept()
        
        y = threading.Thread(target=ListeningLoop, args=(conn,))
        y.start()
        buffer = str(alice.public_key)
        sendport.send(buffer.encode("utf-8"))
        p = Packet()
        while True:
            a = input("Alice:")
            p = alice.encrypt_message(a)
            sendport.send(p.iv_bytes)
            sendport.send(p.encrypted_message)
            print(p.encrypted_message)

