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
            # Create 512 files of 1MB each = 512MB
            for i in range(512):
                with open(f"{self.test_folder}/file_{i}", "wb") as file:
                    file.write(os.urandom(1024*1024))

    def tearDown(self) -> None:
        if os.path.exists(self.test_folder):
            shutil.rmtree(self.test_folder)


    def test_locker_with_tarfile(self):
        import time
        import locker
        import crypto
        
        archiver = get_archiver("tarfile")
        crypto = crypto.Crypto()
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
        crypto = crypto.Crypto()
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
        crypto = crypto.Crypto()
        locker = locker.Locker(archiver, crypto)
        start = time.time()
        encrypted_file = locker.lock_folder(self.test_folder,  "password", ".")
        end = time.time()

        print(f"Time taken for zipfile locking: {end - start} seconds")

        self.assertTrue(os.path.exists(f"{self.test_folder}.zip.enc"))

        os.rename(encrypted_file, f"{encrypted_file}_zipfile")



    def test_locker_with_custom(self):
        import time
        import locker
        import crypto

        archiver = get_archiver("custom")
        crypto = crypto.Crypto()
        locker = locker.Locker(archiver, crypto)
        start = time.time()
        encrypted_file = locker.lock_folder(self.test_folder,  "password", ".")
        end = time.time()

        print(f"Time taken for custom locking: {end - start} seconds")

        self.assertTrue(os.path.exists(f"{self.test_folder}.archive.enc"))

        os.rename(encrypted_file, f"{encrypted_file}_custom")



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
        crypto = crypto.Crypto()
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
        crypto = crypto.Crypto()
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
        crypto = crypto.Crypto()
        locker = locker.Locker(archiver, crypto)
        encrypted_file = "test_folder.zip.enc_zipfile"
        start = time.time()
        unlocked_folder = locker.unlock_folder(encrypted_file, "password", self.test_out_folder)
        end = time.time()

        print(f"Time taken for zipfile unlocking: {end - start} seconds")
        self.assertTrue(os.path.exists(unlocked_folder))
        shutil.rmtree(unlocked_folder)
        os.remove(encrypted_file)


    def test_unlocker_with_custom(self):
        import locker
        import crypto
        import os
        import time
        archiver = get_archiver("custom")
        crypto = crypto.Crypto()
        locker = locker.Locker(archiver, crypto)
        encrypted_file = "test_folder.archive.enc_custom"
        start = time.time()
        unlocked_folder = locker.unlock_folder(encrypted_file, "password", self.test_out_folder)
        end = time.time()

        print(f"Time taken for custom unlocking: {end - start} seconds")
        self.assertTrue(os.path.exists(unlocked_folder))
        shutil.rmtree(unlocked_folder)
        os.remove(encrypted_file)




if __name__ == "__main__":
    unittest.main()    

