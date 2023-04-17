import socket, pickle
import threading
from Diffie_Hellman_Merkle import *
HOST = "127.0.0.1" 
alice = DiffieHellman()
alice.set_public_key()
fragments = []

def ListeningLoop(conn):
    p = Packet()
    buffer = conn.recv(1024)
    buffer = int(buffer.decode("utf-8"))
    alice.set_private_key(buffer)
    print("Shared Key:",alice.shared_key)
    buffer = ""
    while True:
        buffer = conn.recv(4096)
        p = pickle.loads(buffer)
        p.string_message = alice.decrypt_message(p.encrypted_message, p.iv_bytes, p.signature)
        print()
        print("From: Bob - ", p.string_message)

if __name__ == "__main__":
    mode = ""
    message = []
    while (mode != "Y" and mode != "N"):
        mode = input("Would you like to run in evesdropping mode? (Y/N)")
    if mode == "N":
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sendport:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as receiveport:
                SecureChannel = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                SecureChannel.bind((HOST, SECUREALICE))
                SecureChannel.connect((HOST, SECUREBOB))
                buffer = pickle.dumps(alice.MYVK)
                SecureChannel.send(buffer)
                buffer = ""
                while 1:
                    SecureChannel.settimeout(.5)
                    try:
                        buffer = SecureChannel.recv(4096)
                    except:
                        pass

                    if buffer == b'':
                        break
                    if buffer != "":
                        message.append(buffer)
                    buffer = b''
                message = b''.join(message)
                alice.OtherVK = pickle.loads(message)
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
                    packet = pickle.dumps(p)
                    sendport.send(packet)
    else:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sendport:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as receiveport:
                SecureChannel = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                SecureChannel.bind((HOST, SECUREALICE))
                SecureChannel.connect((HOST, SECUREBOB))
                buffer = pickle.dumps(alice.MYVK)
                SecureChannel.send(buffer)
                buffer = ""
                while 1:
                    SecureChannel.settimeout(3)
                    try:
                        buffer = SecureChannel.recv(4096)
                    except:
                        pass

                    if buffer == b'':
                        break
                    if buffer != "":
                        message.append(buffer)
                    buffer = b''
                message = b''.join(message)
                alice.OtherVK = pickle.loads(message)
                sendport.bind((HOST, ALICESEND))
                sendport.connect((HOST,ALICEtoEVEPORT))
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
                    packet = pickle.dumps(p)
                    sendport.send(packet)
        

