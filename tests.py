import os
import unittest
from archiver import get_archiver
import shutil


class TestLocker(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.test_folder = "test_folder"

    def setUp(self) -> None:
        if not os.path.exists(self.test_folder):
            os.makedirs(self.test_folder)
            # create a test folder with files of random size, the folder size should be around 1 gib
            file_distribution = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100] # = 550 mb

            for i in file_distribution:
                with open(f"{self.test_folder}/file_{i}.txt", "wb") as f:
                    f.write(os.urandom(1024 * 1024 * i))
            
    
    def tearDown(self) -> None:
        if os.path.exists(self.test_folder):
            shutil.rmtree(self.test_folder)


    def test_locker_with_tarfile(self):
        import time
        import locker
        import crypto
        
        archiver = get_archiver("tarfile")
        crypto = crypto.FileCrypto()
        locker = locker.Locker(archiver, crypto)
        start = time.time()
        encrypted_file = locker.lock_folder(self.test_folder,  "password", ".")
        end = time.time()

        print(f"Time taken for tarfile locking: {end - start} seconds")

        self.assertTrue(os.path.exists(f"{self.test_folder}.tar.enc"))

        os.rename(encrypted_file, f"{encrypted_file}_tarfile")

    def test_locker_with_shutil(self):
        import time
        import locker
        import crypto
        
        archiver = get_archiver("shutil")
        crypto = crypto.FileCrypto()
        locker = locker.Locker(archiver, crypto)
        start = time.time()
        encrypted_file = locker.lock_folder(self.test_folder,  "password", ".")
        end = time.time()

        print(f"Time taken for shutil locking: {end - start} seconds")

        self.assertTrue(os.path.exists(f"{self.test_folder}.tar.enc"))
        os.rename(encrypted_file, f"{encrypted_file}_shutil")


    def test_locker_with_zipfile(self):
        import time
        import locker
        import crypto
        
        archiver = get_archiver("zipfile")
        crypto = crypto.FileCrypto()
        locker = locker.Locker(archiver, crypto)
        start = time.time()
        encrypted_file = locker.lock_folder(self.test_folder,  "password", ".")
        end = time.time()

        print(f"Time taken for zipfile locking: {end - start} seconds")

        self.assertTrue(os.path.exists(f"{self.test_folder}.zip.enc"))

        os.rename(encrypted_file, f"{encrypted_file}_zipfile")



    def test_locker_with_pickle(self):
        import time
        import locker
        import crypto

        archiver = get_archiver("pickle")
        crypto = crypto.FileCrypto()
        locker = locker.Locker(archiver, crypto)
        start = time.time()
        encrypted_file = locker.lock_folder(self.test_folder,  "password", ".")
        end = time.time()

        print(f"Time taken for pickle locking: {end - start} seconds")

        self.assertTrue(os.path.exists(f"{self.test_folder}.archive.enc"))

        os.rename(encrypted_file, f"{encrypted_file}_pickle")


    def test_locker_with_json(self):
        import time
        import locker
        import crypto

        archiver = get_archiver("json")
        crypto = crypto.FileCrypto()
        locker = locker.Locker(archiver, crypto)
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
        import locker
        import crypto
        import os
        import time

        archiver = get_archiver("tarfile")
        crypto = crypto.FileCrypto()
        locker = locker.Locker(archiver, crypto)
        encrypted_file = "test_folder.tar.enc_tarfile"
        start = time.time()
        unlocked_folder = locker.unlock_folder(encrypted_file, "password", self.test_out_folder)
        end = time.time()

        print(f"Time taken for tarfile unlocking: {end - start} seconds")

        self.assertTrue(os.path.exists(unlocked_folder))
        shutil.rmtree(unlocked_folder)
        os.remove(encrypted_file)

    def test_unlocker_with_shutil(self):
        import locker
        import crypto
        import os
        import time


        archiver = get_archiver("shutil")
        crypto = crypto.FileCrypto()
        locker = locker.Locker(archiver, crypto)
        encrypted_file = "test_folder.tar.enc_shutil"
        start = time.time()
        unlocked_folder = locker.unlock_folder(encrypted_file, "password", self.test_out_folder)
        end = time.time()

        print(f"Time taken for shutil unlocking: {end - start} seconds")
        self.assertTrue(os.path.exists(unlocked_folder))
        shutil.rmtree(unlocked_folder)
        os.remove(encrypted_file)


    def test_unlocker_with_zipfile(self):
        import locker
        import crypto
        import os
        import time
        archiver = get_archiver("zipfile")
        crypto = crypto.FileCrypto()
        locker = locker.Locker(archiver, crypto)
        encrypted_file = "test_folder.zip.enc_zipfile"
        start = time.time()
        unlocked_folder = locker.unlock_folder(encrypted_file, "password", self.test_out_folder)
        end = time.time()

        print(f"Time taken for zipfile unlocking: {end - start} seconds")
        self.assertTrue(os.path.exists(unlocked_folder))
        shutil.rmtree(unlocked_folder)
        os.remove(encrypted_file)


    def test_unlocker_with_pickle(self):
        import locker
        import crypto
        import os
        import time
        archiver = get_archiver("pickle")
        crypto = crypto.FileCrypto()
        locker = locker.Locker(archiver, crypto)
        encrypted_file = "test_folder.archive.enc_pickle"
        start = time.time()
        unlocked_folder = locker.unlock_folder(encrypted_file, "password", self.test_out_folder)
        end = time.time()

        print(f"Time taken for pickle unlocking: {end - start} seconds")
        self.assertTrue(os.path.exists(unlocked_folder))
        shutil.rmtree(unlocked_folder)
        os.remove(encrypted_file)

    def test_unlocker_with_json(self):
        import locker
        import crypto
        import os
        import time
        archiver = get_archiver("json")
        crypto = crypto.FileCrypto()
        locker = locker.Locker(archiver, crypto)
        encrypted_file = "test_folder.json.enc_json"
        start = time.time()
        unlocked_folder = locker.unlock_folder(encrypted_file, "password", self.test_out_folder)
        end = time.time()

        print(f"Time taken for json unlocking: {end - start} seconds")
        self.assertTrue(os.path.exists(unlocked_folder))
        shutil.rmtree(unlocked_folder)
        os.remove(encrypted_file)



if __name__ == "__main__":
    unittest.main()