
import time
import unittest
from archiver import get_archiver
import shutil
from crypto import FileCrypto, Crypto
from locker import Locker
import os


class TestCrypto(unittest.TestCase):
    def test_encrypt_decrypt_data(self):
        crypto = Crypto()
        data = b"hello world"
        password = "password"
        encrypted_data = crypto.encrypt(password.encode(), data)
        decrypted_data = crypto.decrypt(password.encode(), encrypted_data)
        self.assertEqual(data, decrypted_data)

    def test_encrypt_decrypt_file(self):
        crypto = FileCrypto()
        data = b"hello world"
        password = "password"
        with open("test.txt", "wb") as f:
            f.write(data)

        file_hash = crypto.hash_file("test.txt")

        encrypted_file = crypto.encrypt_file(password.encode(), "test.txt", ".")
        os.remove("test.txt")
        decrypted_file = crypto.decrypt_file(password.encode(), encrypted_file, "test.txt")

        decrypted_file_hash = crypto.hash_file(decrypted_file)

        self.assertEqual(file_hash, decrypted_file_hash)
        os.remove(encrypted_file)
        os.remove("test.txt")


class TestLocker(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.test_folder = "test_folder"

    def setUp(self) -> None:
        if not os.path.exists(self.test_folder):
            os.makedirs(self.test_folder)
            # create a test folder with files of random size, the folder size should be around 1 gib
            file_distribution = [10, 20, 30, 40,
                                 50, 60, 70, 80, 90, 100]  # = 550 mb

            for i in file_distribution:
                with open(f"{self.test_folder}/file_{i}.txt", "wb") as f:
                    f.write(os.urandom(1024 * 1024 * i))

    def tearDown(self) -> None:
        if os.path.exists(self.test_folder):
            shutil.rmtree(self.test_folder)

    def test_locker_with_tarfile(self):

        archiver = get_archiver("tarfile")
        crypto = FileCrypto()
        locker = Locker(archiver, crypto)
        start = time.time()
        encrypted_file = locker.lock_folder(self.test_folder,  "password", ".")
        end = time.time()

        print(f"Time taken for tarfile locking: {end - start} seconds")

        self.assertTrue(os.path.exists(f"{self.test_folder}.tar.enc"))

        os.rename(encrypted_file, f"{encrypted_file}_tarfile")

    def test_locker_with_shutil(self):

        archiver = get_archiver("shutil")
        crypto = FileCrypto()
        locker = Locker(archiver, crypto)
        start = time.time()
        encrypted_file = locker.lock_folder(self.test_folder,  "password", ".")
        end = time.time()

        print(f"Time taken for shutil locking: {end - start} seconds")

        self.assertTrue(os.path.exists(f"{self.test_folder}.tar.enc"))
        os.rename(encrypted_file, f"{encrypted_file}_shutil")

    def test_locker_with_zipfile(self):

        archiver = get_archiver("zipfile")
        crypto = FileCrypto()
        locker = Locker(archiver, crypto)
        start = time.time()
        encrypted_file = locker.lock_folder(self.test_folder,  "password", ".")
        end = time.time()

        print(f"Time taken for zipfile locking: {end - start} seconds")

        self.assertTrue(os.path.exists(f"{self.test_folder}.zip.enc"))

        os.rename(encrypted_file, f"{encrypted_file}_zipfile")

    def test_locker_with_pickle(self):

        archiver = get_archiver("pickle")
        crypto = FileCrypto()
        locker = Locker(archiver, crypto)
        start = time.time()
        encrypted_file = locker.lock_folder(self.test_folder,  "password", ".")
        end = time.time()

        print(f"Time taken for pickle locking: {end - start} seconds")

        self.assertTrue(os.path.exists(f"{self.test_folder}.archive.enc"))

        os.rename(encrypted_file, f"{encrypted_file}_pickle")

    def test_locker_with_json(self):

        archiver = get_archiver("json")
        crypto = FileCrypto()
        locker = Locker(archiver, crypto)
        start = time.time()
        encrypted_file = locker.lock_folder(self.test_folder,  "password", ".")
        end = time.time()

        print(f"Time taken for json locking: {end - start} seconds")

        self.assertTrue(os.path.exists(f"{self.test_folder}.json.enc"))

        os.rename(encrypted_file, f"{encrypted_file}_json")


class TestUnlocker(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.test_out_folder = "test_out_folder"

    def test_unlocker_with_tarfile(self):
        archiver = get_archiver("tarfile")
        crypto = FileCrypto()
        locker = Locker(archiver, crypto)
        encrypted_file = "test_folder.tar.enc_tarfile"
        start = time.time()
        unlocked_folder = locker.unlock_folder(
            encrypted_file, "password", self.test_out_folder)
        end = time.time()

        print(f"Time taken for tarfile unlocking: {end - start} seconds")

        self.assertTrue(os.path.exists(unlocked_folder))
        shutil.rmtree(unlocked_folder)
        os.remove(encrypted_file)

    def test_unlocker_with_shutil(self):
        archiver = get_archiver("shutil")
        crypto = FileCrypto()
        locker = Locker(archiver, crypto)
        encrypted_file = "test_folder.tar.enc_shutil"
        start = time.time()
        unlocked_folder = locker.unlock_folder(
            encrypted_file, "password", self.test_out_folder)
        end = time.time()

        print(f"Time taken for shutil unlocking: {end - start} seconds")
        self.assertTrue(os.path.exists(unlocked_folder))
        shutil.rmtree(unlocked_folder)
        os.remove(encrypted_file)

    def test_unlocker_with_zipfile(self):

        archiver = get_archiver("zipfile")
        crypto = FileCrypto()
        locker = Locker(archiver, crypto)
        encrypted_file = "test_folder.zip.enc_zipfile"
        start = time.time()
        unlocked_folder = locker.unlock_folder(
            encrypted_file, "password", self.test_out_folder)
        end = time.time()

        print(f"Time taken for zipfile unlocking: {end - start} seconds")
        self.assertTrue(os.path.exists(unlocked_folder))
        shutil.rmtree(unlocked_folder)
        os.remove(encrypted_file)

    def test_unlocker_with_pickle(self):

        archiver = get_archiver("pickle")
        crypto = FileCrypto()
        locker = Locker(archiver, crypto)
        encrypted_file = "test_folder.archive.enc_pickle"
        start = time.time()
        unlocked_folder = locker.unlock_folder(
            encrypted_file, "password", self.test_out_folder)
        end = time.time()

        print(f"Time taken for pickle unlocking: {end - start} seconds")
        self.assertTrue(os.path.exists(unlocked_folder))
        shutil.rmtree(unlocked_folder)
        os.remove(encrypted_file)

    def test_unlocker_with_json(self):

        archiver = get_archiver("json")
        crypto = FileCrypto()
        locker = Locker(archiver, crypto)
        encrypted_file = "test_folder.json.enc_json"
        start = time.time()
        unlocked_folder = locker.unlock_folder(
            encrypted_file, "password", self.test_out_folder)
        end = time.time()

        print(f"Time taken for json unlocking: {end - start} seconds")
        self.assertTrue(os.path.exists(unlocked_folder))
        shutil.rmtree(unlocked_folder)
        os.remove(encrypted_file)


if __name__ == "__main__":
    unittest.main()
