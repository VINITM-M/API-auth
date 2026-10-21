
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
from core import config 
import base64
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import re
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend


class AESCipher: 

    def __init__(self, data:str):
        self.data = data 
        self.key = config.secret  

    def generating_private_key(self):

        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        
        return private_key 