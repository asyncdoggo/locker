import os
import tarfile

def archive(src, dst):
    # convert src folder to .tar using the fastest compression
    with tarfile.open(dst, "w") as tar:
        tar.add(src, arcname=os.path.basename(src))

def unarchive(file, folder):
    # extract tar file to folder
    with tarfile.open(file, "r") as tar:
        tar.extractall(folder, filter="data")
