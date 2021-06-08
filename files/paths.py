import re
import os
import sys

windows = True if "win" in sys.platform else False

def make_absolute(path : str):
    if path[0] != "/":
        return "/" + path
    return path

# remove the ./ at the beggining of a file of a path
def remove_dot_slash(path : str) -> str:
    return re.sub(r"\^./|^C:/|^C:\\", r"", path)


# if os is windows, this function converts the path to unix format
def path_conversion(path : str, windows : bool) -> str:
    if windows:
        return re.sub(r"\\", r"/", path)
    return path

def get_cwd():
    path = os.getcwd()
    path = remove_dot_slash(path_conversion(path, windows))
    return make_absolute(path)

def convert_path(path):
    path = path_conversion(remove_dot_slash(path), windows)
    return make_absolute(path)

# splits the full path and returns the path and file/folder name as a two item tuple
def path_name(path) -> tuple:
    array = path.split("/")
    if len(array) == 1:
        return "", array[0]
    return ("/".join(array[0:len(array)-1]), array[len(array)-1])

# runs all the above functions in one go
def path(path: str, windows: bool) -> tuple:
    path, name = path_name(remove_dot_slash(path_conversion(path, windows)))
    return path, name