import os
from shutil import copyfile


def extract(filename):
    if not os.path.isfile(f"./{filename}.exe"):
        copyfile(f"./{filename}", f"./{filename}.exe")


extract("EasyScopeX_setup")
extract("MiniMouseMacro")
