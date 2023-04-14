import socket
import threading
from Diffie_Hellman_Merkle import *
from copy import deepcopy
from time import sleep
HOST = "127.0.0.1" 
BobFake = DiffieHellman()
BobFake.set_public_key()

AliceFake = DiffieHellman()
AliceFake.set_public_key()

def ListeningLoopAlice(Aconn, Bconn):
    p = Packet()
    buffer = Aconn.recv(1024)
    buffer = int(buffer.decode("utf-8"))
    AliceFake.set_private_key(buffer)
    print(AliceFake.shared_key)
    while True:
        p.iv_bytes = Aconn.recv(16)
        p.encrypted_message = Aconn.recv(1024)
        p.string_message = buffer = AliceFake.decrypt_message(p.encrypted_message, p.iv_bytes)
        p = BobFake.encrypt_message(p.string_message)
        Bconn.send(p.iv_bytes)
        Bconn.send(p.encrypted_message)
        print(buffer)
        

def ListeningLoopBob(Aconn, Bconn):
    p = Packet()
    p1 = deepcopy(p)
    buffer = Aconn.recv(1024)
    buffer = int(buffer.decode("utf-8"))
    BobFake.set_private_key(buffer)
    print(BobFake.shared_key)
    while True:
        p.iv_bytes = Aconn.recv(16)
        p.encrypted_message = Aconn.recv(1024)
        p.string_message = buffer = BobFake.decrypt_message(p.encrypted_message, p.iv_bytes)
        p = AliceFake.encrypt_message(p.string_message)
        Bconn.send(p.iv_bytes)
        Bconn.send(p.encrypted_message)
        print(buffer)


EvetoBob = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
EvetoAlice = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
AlicetoEve = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
BobtoEve = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


AlicetoEve.bind((HOST, ALICEtoEVEPORT))
EvetoAlice.bind((HOST, EVEtoALICEPORT))
AlicetoEve.listen()
Aliceconn, addr = AlicetoEve.accept()
EvetoAlice.connect((HOST, ALICELISTEN))
buffer = str(AliceFake.public_key)
EvetoAlice.send(buffer.encode("utf-8"))
BobtoEve.bind((HOST, BOBtoEVEPORT))
EvetoBob.bind((HOST, EVEtoBOBPORT))
BobtoEve.listen()
Bobconn, addr = BobtoEve.accept()
EvetoBob.connect((HOST, BOBLISTEN))
buffer = str(BobFake.public_key)
EvetoBob.send(buffer.encode("utf-8"))
y = threading.Thread(target=ListeningLoopAlice, args=(Aliceconn,EvetoBob,))
y.start()
x = threading.Thread(target=ListeningLoopBob, args=(Bobconn,EvetoAlice))
x.start()

