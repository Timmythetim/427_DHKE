#This is just a basic implementation of DiffieHellman with fixed g and p for simplicity
#We will assume that the Diffie Hellman Algorithm is secure for this demonstartion,
#As it focuses more on the MitM attack
import random
from ecdsa import SigningKey
from Crypto.Cipher import AES
class DiffieHellman:
    def __init__(self):
        self.p = 129866728583
        self.g = 12345
        self.secret_value = random.randint(0,10000)
        self.public_key = 0
        self.shared_key = 0
        self.SK = SigningKey.generate()
        self.MYVK = self.SK.verifying_key
        #this will be recieved from the other party and saved
        self.OtherVK = 0
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
        signature = self.SK.sign(cipher_text)
        return Packet(iv,cipher_text,signature)
    def decrypt_message(self, message, iv, signature):
        decypt_cipher = AES.new(self.shared_key.to_bytes(16, 'big'), AES.MODE_OFB, iv = iv)
        plain_text = decypt_cipher.decrypt(message)
        plain_text = plain_text.decode("utf-8")
        try:
            self.OtherVK.verify(signature, message)
        except:
            plain_text = "Message integrity could not be verified"
        return plain_text
    
class Packet:
    def __init__(self, iv = b'', encrypted_message=b'', signature = b''):
        self.iv_bytes = iv
        self.encrypted_message = encrypted_message
        self.string_message = ""
        self.signature = signature
    
        
        
ALICELISTEN = 45001
ALICESEND = 45000
BOBLISTEN = 45002
BOBSEND = 45003
EVEtoBOBPORT = 45004
BOBtoEVEPORT = 45005
EVEtoALICEPORT = 45006
ALICEtoEVEPORT = 45007
SECUREALICE = 45008
SECUREBOB = 45009
