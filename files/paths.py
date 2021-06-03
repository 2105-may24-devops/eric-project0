import re

# remove the ./ at the beggining of a file of a path
def remove_dot_slash(path : str) -> str:
    return re.sub(r"\./", r"", path)

# if os is windows, this function converts the path to unix format
def path_conversion(path : str, windows : bool) -> str:
    if windows:
        return re.sub(r"\\", r"/", path)
    return path

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