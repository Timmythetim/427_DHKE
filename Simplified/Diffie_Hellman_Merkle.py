#This is just a basic implementation of DiffieHellman with fixed g and p for simplicity
#We will assume that the Diffie Hellman Algorithm is secure for this demonstartion,
#As it focuses more on the MitM attack
import random
from Crypto.Cipher import AES
class DiffieHellman:
    def __init__(self):
        #Assume we are in Z_199 space
        self.p = 199
        self.g = 127
        self.secret_value = random.randint(0,199)
        self.public_key = 0
        self.shared_key = 0
        self.AESKey = 0
    #For use by the server
    def set_public_key(self):
        self.public_key = ((self.g ** self.secret_value) % self.p)
    def set_private_key(self,public_key):
        self.shared_key = (public_key ** self.secret_value) % self.p
    def encrypt_message(self, message):
        key = self.shared_key
        cipher = AES.new(key.to_bytes(16, 'big'),AES.MODE_OFB)
        cipher_text = cipher.encrypt(message.encode("utf-8"))
        iv = cipher.iv
        return Packet(iv,cipher_text)
    def decrypt_message(self, message, iv):
        decypt_cipher = AES.new(self.shared_key.to_bytes(16, 'big'), AES.MODE_OFB, iv = iv)
        plain_text = decypt_cipher.decrypt(message)
        plain_text = plain_text.decode("utf-8")
        return plain_text
    
class Packet:
    def __init__(self, iv = b'', encrypted_message=b''):
        self.iv_bytes = iv
        self.encrypted_message = encrypted_message
        self.string_message = ""
    
        
        
ALICELISTEN = 45001
ALICESEND = 45000
BOBLISTEN = 45002
BOBSEND = 45003
EVEtoBOBPORT = 45004
BOBtoEVEPORT = 45005
EVEtoALICEPORT = 45006
ALICEtoEVEPORT = 45007
