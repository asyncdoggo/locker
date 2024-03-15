import os
from crypto import Crypto
from archiver import Archiver
from Cryptodome.Protocol.KDF import PBKDF2


class Locker:
    def __init__(self, archiver: Archiver, crypto: Crypto):
        self.archiver = archiver
        self.crypto = crypto

    def lock_folder(self, folder: str, password: str, out_folder: str) -> str:
        key = self.crypto.generate_key(password)
        self.archiver.archive(folder, f"{folder}.tar")
        encrypted_archive = self.crypto.encrypt_file(key, f"{folder}.tar", out_folder)
        os.remove(f"{folder}.tar")
        return encrypted_archive
       
    def unlock_folder(self, file: str, password: str, out_folder: str =".") -> str:
        key = self.crypto.generate_key(password)
        decrypted_archive = self.crypto.decrypt_file(key, file)
        self.archiver.unarchive(decrypted_archive, out_folder)
        os.remove(decrypted_archive)
        return out_folder


