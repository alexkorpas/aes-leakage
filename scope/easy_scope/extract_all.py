import os
from shutil import copyfile


def extract(filename):
    if not os.path.isfile(f"./{filename}.exe"):
        copyfile(f"./{filename}", f"./{filename}.exe")


extract("EasyScopeX_setup") # https://mediacdn.eu/mage/media/wysiwyg/siglent/Downloads/Software/EasyScopeX_V100R001B02D01P20.zip
extract("MiniMouseMacro")
