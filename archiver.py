import os
import shutil
import tarfile
import zipfile


class Archiver:
    def __init__(self):
        pass

    def archive(self, src: str, dst: str=None) -> str:
        pass

    def unarchive(self, file: str, folder: str):
        pass



class TarfileArchiver(Archiver):
    def archive(self, src: str, dst: str = None) -> str:
        if not dst:
            dst = src + ".tar"
        with tarfile.open(dst, "x:") as tar:
            tar.add(src, arcname=os.path.basename(src))

        return dst

    def unarchive(self, file: str, folder: str) -> None:
        with tarfile.open(file, "r:") as tar:
            tar.extractall(folder, filter="data")

class ShutilArchiver(Archiver):
    def archive(self, src: str, dst: str = None) -> str:
        if not dst:
            # shutil automatically appends the extension
            dst = src
        shutil.make_archive(dst, "tar", src)

        return dst + ".tar"

    def unarchive(self, file: str, folder: str) -> None:
        shutil.unpack_archive(file, folder)



class ZipfileArchiver(Archiver):
    def archive(self, src: str, dst: str = None) -> str:
        if not dst:
            dst = src + ".zip"
        with zipfile.ZipFile(dst, "x", compression=zipfile.ZIP_STORED) as zipf:
            for root, dirs, files in os.walk(src):
                for file in files:
                    zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), src))

        return dst

    def unarchive(self, file: str, folder: str) -> None:
        with zipfile.ZipFile(file, "r") as zipf:
            zipf.extractall(folder)
            

def get_archiver(archiver: str) -> Archiver:
    if archiver == "tarfile":
        return TarfileArchiver()
    elif archiver == "shutil":
        return ShutilArchiver()
    elif archiver == "zipfile":
        return ZipfileArchiver()
    else:
        raise ValueError("Invalid archiver")