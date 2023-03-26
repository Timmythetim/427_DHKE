import pyDH
import socket
import sys
import threading
HOST = "127.0.0.1" 
PORT = 45000
# ALICEPORT = 45001
# BOBPORT = 45002
# EVEPORT = 45003

def ProcessingLoop(conn,addr):
    print("Connected to: ",addr)
    while(1):
        a = conn.recv(1024)
        print(a.decode())
        if a.decode() == "quit":
            conn.close()
            break



if __name__ == "__main__":
# d1 = pyDH.DiffieHellman()
# d2 = pyDH.DiffieHellman()
# d1_pubkey = d1.gen_public_key()
# d2_pubkey = d2.gen_public_key()
# d1_sharedkey = d1.gen_shared_key(d2_pubkey)
# d2_sharedkey = d2.gen_shared_key(d1_pubkey)
# d1_sharedkey == d2_sharedkey
# print(d1_pubkey)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        while(1):
            s.listen()
            conn, addr = s.accept()
            print("Hello!")
            x = threading.Thread(target=ProcessingLoop, args=(conn, addr,))
            x.start()

