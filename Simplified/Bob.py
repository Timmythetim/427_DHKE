import socket, pickle
import threading
from Diffie_Hellman_Merkle import *
HOST = "127.0.0.1" 
bob = DiffieHellman()
bob.set_public_key()
fragments = []
def ListeningLoop(conn):
    buffer = ""
    message = []
    p = Packet()
    buffer = conn.recv(1024)
    buffer = buffer.decode("utf-8")
    buffer = int(buffer)
    bob.set_private_key(buffer)
    print("Shared Key:",bob.shared_key)
    buffer = ""
    while True:
        buffer = conn.recv(4096)
        p = pickle.loads(buffer)
        p.string_message = bob.decrypt_message(p.encrypted_message, p.iv_bytes, p.signature)
        print()
        print("From: Alice - ", p.string_message)
        
        
        
if __name__ == "__main__":
    mode = ""
    message = []
    while (mode != "Y" and mode != "N"):
        mode = input("Would you like to run in evesdropping mode? (Y/N)")
    if mode == "N":
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sendport:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as receiveport:
                SecureChannel = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                SecureChannel.bind((HOST, SECUREBOB))
                SecureChannel.listen()
                secConn, addr = SecureChannel.accept()
                while 1:
                    secConn.settimeout(.5)
                    try:
                        buffer = secConn.recv(4096)
                    except:
                        pass
                    if buffer == b'':
                        break
                    if buffer != "":
                        message.append(buffer)
                    buffer = b''
                temp = b''.join(message)
                message = []
                bob.OtherVK = pickle.loads(temp)
                temp = pickle.dumps(bob.MYVK)
                secConn.send(temp)
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
                    packet = pickle.dumps(p)
                    sendport.send(packet)
    else:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sendport:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as receiveport:
                SecureChannel = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                SecureChannel.bind((HOST, SECUREBOB))
                SecureChannel.listen()
                secConn, addr = SecureChannel.accept()
                while 1:
                    secConn.settimeout(3)
                    try:
                        buffer = secConn.recv(4096)
                    except:
                        pass
                    if buffer == b'':
                        break
                    if buffer != "":
                        message.append(buffer)
                    buffer = b''
                temp = b''.join(message)
                message = []
                bob.OtherVK = pickle.loads(temp)
                temp = pickle.dumps(bob.MYVK)
                secConn.send(temp)
                
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
                    packet = pickle.dumps(p)
                    sendport.send(packet)