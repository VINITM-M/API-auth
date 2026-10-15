# AES algorithm — it’s fast, highly secure, and especially suitable for handling large amounts of data.
# AES algorithm suitable for symmetric key encryption, which means the same key is used for both encryption and decryption. It is widely used in various applications, including secure communications, data storage, and more. 


from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
from core import config 


class AESCipher: 

    def __init__(self, data:str):
        self.data = data 
        self.key = config.secret 

    def pad_data(self,data):

        # Pad the data to be a multiple of 16 bytes (AES block size)
        padding_length = 16 - (len(data) % 16)

        # Create the padding bytes
        padding = bytes([padding_length] * padding_length   )
        return data + padding

    def encrypt_data(self):

        padded_data = self.pad_data(self.data.encode('utf-8'))

        # Generate a random IV
        iv = get_random_bytes(16)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)

        # Encrypt the data
        encrypted = cipher.encrypt(padded_data)

        # Combine the IV and the encrypted data
        return base64.b64encode(iv + encrypted)

    def decrypt_data(self, encrypted_data):

        # Base64 decode
        raw = base64.b64decode(encrypted_data)

        # Extract IV
        iv = raw[:16]

        # Extract ciphertext
        encrypted = raw[16:]

        # Create the cipher for decryption
        cipher = AES.new(key, AES.MODE_CBC, iv)

        # Decrypt
        decrypted = cipher.decrypt(encrypted)

        # Remove padding
        pad_len = decrypted[-1]

        return decrypted[:-pad_len]
