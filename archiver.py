import os
import shutil
import tarfile
import zipfile
import pickle

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
            


class CustomArchiver(Archiver):
    def archive(self, src: str, dst: str = None) -> str:
        structure = {}
        for dir, subdir, files in os.walk(src):
            structure[dir] = {}

            for file in files:
                with open(os.path.join(dir,file), 'rb') as fp:
                    file_content = fp.read()
                    structure[dir][file] = file_content

        if not dst:
            dst = src + ".archive"
        
        with open(dst, 'wb') as fp:
            pickle.dump(structure, fp, pickle.HIGHEST_PROTOCOL)

        return dst


    def unarchive(self, file: str, folder: str):
        os.makedirs(folder)

        with open(file, 'rb') as fp:
            structure = pickle.load(fp)
        

        for dir,files in structure.items():
            os.makedirs(os.path.join(folder, dir), exist_ok=True)

            for file,content in files.items():
                with open(os.path.join(folder, dir, file), 'wb') as fp:
                    fp.write(content)

        




def get_archiver(archiver: str) -> Archiver:
    if archiver == "tarfile":
        return TarfileArchiver()
    elif archiver == "shutil":
        return ShutilArchiver()
    elif archiver == "zipfile":
        return ZipfileArchiver()
    elif archiver == "custom":
        return CustomArchiver()
    else:
        raise ValueError("Invalid archiver")
    


if __name__ == "__main__":
    archiver = get_archiver("custom")
    # archiver.archive("testing")
    archiver.unarchive("testing.archive", "test_out")