# archiver has been created to archive the files in the given directory
# crypto has been created to encrypt and decrypt files
# steps to lock folder
# 1. archive the folder
# 2. encrypt the archive
# 3. delete the archive
#
# steps to unlock folder
# 1. decrypt the archive
# 2. unarchive the archive
# 3. delete the archive
#

import os
from random import randbytes
from crypto import encrypt_file, decrypt_file, hash_file
from archiver import archive, unarchive
from Cryptodome.Protocol.KDF import PBKDF2


def lock_folder(folder, password):
    # Lock the folder using the given password
    key = PBKDF2(password, b'salt', dkLen=32, count=1000000)
    archive(folder, f"{folder}.tar")
    encrypted_archive = encrypt_file(key, f"{folder}.tar")
    os.remove(f"{folder}.tar")
    return encrypted_archive


def unlock_folder(file, password, out_folder="."):
    # Unlock the folder using the given
    key = PBKDF2(password, b'salt', dkLen=32, count=1000000)
    decrypted_archive = decrypt_file(key, file)
    unarchive(decrypted_archive, out_folder)
    os.remove(decrypted_archive)
    return file.replace(".tar.enc", "")

