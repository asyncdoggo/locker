# crypto module using pycryptodomex

import os
import hashlib
from Cryptodome.Cipher import AES
from Cryptodome.Protocol.KDF import PBKDF2
from Cryptodome.Util.Padding import pad, unpad



class Crypto:
    def encrypt_file(self, key: bytes, in_filename: str, out_folder: str=None) -> str:
        if not out_folder:
            out_folder = os.path.dirname(in_filename)

        out_filename = os.path.join(out_folder, os.path.basename(in_filename) + ".enc")
        with open(in_filename, "rb") as in_file:
            data = in_file.read()
        cipher = AES.new(key, AES.MODE_CBC)
        iv = cipher.iv
        ciphertext = cipher.encrypt(pad(data, AES.block_size))
        with open(out_filename, "wb") as out_file:
            out_file.write(iv)
            out_file.write(ciphertext)
        return out_filename

    def decrypt_file(self, key: bytes, in_filename: str, out_filename: str=None) -> str:
        if not out_filename:
            out_filename = os.path.splitext(in_filename)[0]
        with open(in_filename, "rb") as in_file:
            iv = in_file.read(AES.block_size)
            ciphertext = in_file.read()
        cipher = AES.new(key, AES.MODE_CBC, iv)
        data = unpad(cipher.decrypt(ciphertext), AES.block_size)
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
    
    def generate_key(self, password: str) -> bytes:
        return PBKDF2(password, b"salt", 32, 1000000)    