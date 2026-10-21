# AES algorithm — it’s fast, highly secure, and especially suitable for handling large amounts of data.
# AES algorithm suitable for symmetric key encryption, which means the same key is used for both encryption and decryption. It is widely used in various applications, including secure communications, data storage, and more. 


from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
from core import config 
import base64
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import re

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
        padded_data = self.pad_data(self.data.encode("utf-8"))

        # Generate a random IV
        iv = get_random_bytes(16)

        cipher = AES.new(self.key, AES.MODE_CBC, iv)

        # Encrypt the padded data
        encrypted = cipher.encrypt(padded_data)

        # Combine IV and ciphertext, then encode as Base64
        return base64.b64encode(iv + encrypted).decode("ascii")

    def decrypt_data(self, encrypted_data):
        
        # Step 1: Convert input to string if it is bytes
        if isinstance(encrypted_data, bytes):
            encrypted_data = encrypted_data.decode("ascii")

        encrypted_data = encrypted_data.strip()

        # Step 2: Detect hexadecimal-encoded Base64 input
        if encrypted_data.startswith(r"\x"):
            hex_data = encrypted_data[2:]

            if len(hex_data) % 2 != 0 or not re.fullmatch(
                r"[0-9a-fA-F]+", hex_data
            ):
                raise ValueError("Invalid hexadecimal input")

            encrypted_data = bytes.fromhex(hex_data).decode("ascii")

        # Step 3: Decode Base64
        try:
            raw = base64.b64decode(encrypted_data, validate=True)
        except Exception as exc:
            raise ValueError(
                "Invalid Base64 data. Check whether the input is corrupted."
            ) from exc

        # Step 4: Validate IV and ciphertext
        if len(raw) < 32:
            raise ValueError("Encrypted data is too short")

        iv = raw[:16]
        encrypted = raw[16:]

        if len(encrypted) % AES.block_size != 0:
            raise ValueError("Invalid AES ciphertext length")

        # Step 5: AES-CBC decryption
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        decrypted = cipher.decrypt(encrypted)

        # Step 6: Remove PKCS#7 padding
        pad_len = decrypted[-1]

        if not 1 <= pad_len <= AES.block_size:
            raise ValueError("Invalid padding or incorrect encryption key")

        if decrypted[-pad_len:] != bytes([pad_len]) * pad_len:
            raise ValueError("Invalid padding or incorrect encryption key")

        # Step 7: Return original text
        return decrypted[:-pad_len].decode("utf-8")
