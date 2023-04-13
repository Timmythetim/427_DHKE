#This is just a basic implementation of DiffieHellman with fixed g and p for simplicity
#We will assume that the Diffie Hellman Algorithm is secure for this demonstartion,
#As it focuses more on the MitM attack
import random
class DiffieHellman:
    def __init__(self):
        #Assume we are in Z_199 space
        self.p = 199
        self.g = 127
        self.secret_value = random.randint(0,199)
        self.public_key = 0
        self.shared_key = 0
    #For use by the server
    def set_public_key(self):
        self.public_key = ((self.g ** self.secret_value) % self.p)
    def set_private_key(self,public_key):
        self.shared_key = (public_key ** self.secret_value) % self.p