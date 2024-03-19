import os
from crypto import FileCrypto
from archiver import Archiver


class Locker:
    def __init__(self, archiver: Archiver, crypto: FileCrypto):
        self.archiver = archiver
        self.crypto = crypto

    def lock_folder(self, folder: str, password: str, out_folder: str) -> str:
        archive_out_path = self.archiver.archive(folder)
        encrypted_archive = self.crypto.encrypt_file(
            password.encode(), archive_out_path, out_folder)
        os.remove(archive_out_path)
        return encrypted_archive
       
    def unlock_folder(self, file: str, password: str, out_folder: str =".") -> str:
        decrypted_archive = self.crypto.decrypt_file(password.encode(), file)
        self.archiver.unarchive(decrypted_archive, out_folder)
        os.remove(decrypted_archive)
        return out_folder


