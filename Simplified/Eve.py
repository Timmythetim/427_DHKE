import socket, pickle
import threading
from Diffie_Hellman_Merkle import *
from copy import deepcopy
from time import sleep
HOST = "127.0.0.1" 
BobFake = DiffieHellman()
BobFake.set_public_key()
BobFake.OtherVK = BobFake.MYVK


AliceFake = DiffieHellman()
AliceFake.set_public_key()
AliceFake.OtherVK = AliceFake.MYVK

def ListeningLoopAlice(Aconn, Bconn):
    p = Packet()
    buffer = Aconn.recv(1024)
    buffer = int(buffer.decode("utf-8"))
    AliceFake.set_private_key(buffer)
    print("Alice's Fake Key: ",AliceFake.shared_key)
    while True:
        buffer = Aconn.recv(4096)
        p = pickle.loads(buffer)
        p.string_message = AliceFake.decrypt_message(p.encrypted_message, p.iv_bytes, p.signature)
        temp = p.string_message
        p = BobFake.encrypt_message(p.string_message)
        p = pickle.dumps(p)
        Bconn.send(p)
        print(temp)
        

def ListeningLoopBob(Aconn, Bconn):
    p = Packet()
    buffer = Aconn.recv(1024)
    buffer = int(buffer.decode("utf-8"))
    BobFake.set_private_key(buffer)
    print("Bob's Fake Key: ",BobFake.shared_key)
    while True:
        buffer = Aconn.recv(4096)
        p = pickle.loads(buffer)
        p.string_message = BobFake.decrypt_message(p.encrypted_message, p.iv_bytes, p.signature)
        temp = p.string_message
        p = AliceFake.encrypt_message(p.string_message)
        p = pickle.dumps(p)
        Bconn.send(p)
        print(temp)


EvetoBob = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
EvetoAlice = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
AlicetoEve = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
BobtoEve = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

BobtoEve.bind((HOST, BOBtoEVEPORT))
EvetoBob.bind((HOST, EVEtoBOBPORT))
print("Listening for Bob!")
BobtoEve.listen()
Bobconn, addr = BobtoEve.accept()
EvetoBob.connect((HOST, BOBLISTEN))
buffer = str(BobFake.public_key)
EvetoBob.send(buffer.encode("utf-8"))

AlicetoEve.bind((HOST, ALICEtoEVEPORT))
EvetoAlice.bind((HOST, EVEtoALICEPORT))
print("Listening for Alice!")
AlicetoEve.listen()
Aliceconn, addr = AlicetoEve.accept()
EvetoAlice.connect((HOST, ALICELISTEN))
buffer = str(AliceFake.public_key)
EvetoAlice.send(buffer.encode("utf-8"))

y = threading.Thread(target=ListeningLoopAlice, args=(Aliceconn,EvetoBob,))
y.start()
x = threading.Thread(target=ListeningLoopBob, args=(Bobconn,EvetoAlice))
x.start()

