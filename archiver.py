import os
import shutil
import tarfile


class Archiver:
    def __init__(self):
        pass

    def archive(self, src: str, dst: str):
        pass

    def unarchive(self, file: str, folder: str):
        pass



class TarfileArchiver(Archiver):
    def archive(self, src: str, dst: str) -> None:
        with tarfile.open(dst, "x:") as tar:
            tar.add(src, arcname=os.path.basename(src))

    def unarchive(self, file: str, folder: str) -> None:
        with tarfile.open(file, "r:") as tar:
            tar.extractall(folder, filter="data")

class ShutilArchiver(Archiver):
    def archive(self, src: str, dst: str) -> None:
        if ".tar" in dst:
            dst = dst.replace(".tar", "")
        shutil.make_archive(dst, "tar", src)

    def unarchive(self, file: str, folder: str) -> None:
        shutil.unpack_archive(file, folder)


