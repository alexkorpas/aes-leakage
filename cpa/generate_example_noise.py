import os

def files_in_dir(dir_name):
    """
    Returns the amount of files in a directory.

    :rtype: int the amount of files in a directory.
    """
    print(os.path.dirname(os.path.abspath(__file__)))
    return len(os.listdir(dir_name))


def next_filename(dir_name, name_prefix, name_suffix):
    return dir_name + name_prefix + str(files_in_dir(dir_name)) + name_suffix


def generate_examples():
    pandas.