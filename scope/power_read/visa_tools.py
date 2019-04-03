import os
import re

import pyvisa
from pyvisa import Resource, VisaIOError


def file_open_append(directory, file_name):
    path = f"{directory}/{file_name}"

    file = open(path, "w")
    file.close()

    file = open(path, "a")
    return file


def fetch_option(title, list_res):
    longest_line = len(title)

    opt = ""
    for i in range(len(list_res)):
        opt_line = f"{i + 1}: {list_res[i]}\n"
        opt += opt_line

        if len(opt_line) > longest_line:
            longest_line = len(opt_line)

    hr = "-" * longest_line
    print(f"{title}\n{hr}\nSelect an option:\n\n{opt}\n{hr}")

    select = input()
    if re.match("[0-9]+", select):
        if 1 <= int(select) <= len(list_res):
            res = list_res[int(select)]
            print(f"Selected {res}.")
            return res

    return fetch_option(title, list_res)


def num_folders(directory):
    return len([x for x in os.walk(directory)])


def get_resource(preferred) -> Resource:
    rm = pyvisa.ResourceManager()
    try:
        res = rm.open_resource(preferred)
    except VisaIOError:
        list_res = rm.list_resources()
        res = rm.open_resource(fetch_option("Tektronix TDS 2022B not found...", list_res))

    return res
