# crypto module using pycryptodomex

import os
import hashlib
from Cryptodome.Cipher import AES
from Cryptodome.Protocol.KDF import PBKDF2
from Cryptodome.Util.Padding import pad, unpad
from Cryptodome.Random import get_random_bytes


class Crypto:
    @staticmethod
    def encrypt(password: bytes, data: bytes) -> bytes:
        salt = get_random_bytes(16)
        key = PBKDF2(password, salt, 32, 1000000)
        cipher = AES.new(key, AES.MODE_CBC)
        iv = cipher.iv
        ciphertext = cipher.encrypt(pad(data, AES.block_size))
        return salt + iv + ciphertext

    @staticmethod
    def decrypt(password: bytes, data: bytes) -> bytes:
        salt = data[:16]
        iv = data[16:16+AES.block_size]
        ciphertext = data[16+AES.block_size:]
        key = PBKDF2(password, salt, 32, 1000000)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(ciphertext), AES.block_size)

    @staticmethod
    def hash(data: bytes) -> str:
        sha256 = hashlib.sha256()
        sha256.update(data)

        return sha256.hexdigest()



class FileCrypto(Crypto):
    def encrypt_file(self, password: bytes, in_filename: str, out_folder: str=None) -> str:
        if not out_folder:
            out_folder = os.path.dirname(in_filename)
        
        out_filename = os.path.join(out_folder, os.path.basename(in_filename) + ".enc")
        with open(in_filename, "rb") as in_file:
            data = in_file.read()
        
        ciphertext = self.encrypt(password, data)
        
        with open(out_filename, "wb") as out_file:
            out_file.write(ciphertext)

        return out_filename

    def decrypt_file(self, password: bytes, in_filename: str, out_filename: str=None) -> str:
        if not out_filename:
            out_filename = os.path.splitext(in_filename)[0]

        with open(in_filename, "rb") as in_file:
            ciphertext = in_file.read()
        data = self.decrypt(password, ciphertext)
        with open(out_filename, "wb") as out_file:
            out_file.write(data)
        return out_filename

    def hash_file(self, filename: str) -> str:
        # Return SHA-256 hash of file
        sha256 = hashlib.sha256()
        with open(filename, "rb") as file:
            while (chunk := file.read(8192)):
                sha256.update(chunk)
        return sha256.hexdigest()
    



if __name__ == "__main__":
    crypto = FileCrypto()
    password = "password".encode()
    filename = "app.py"
    encrypted_filename = crypto.encrypt_file(password, filename)
    print(f"Encrypted file: {encrypted_filename}")


