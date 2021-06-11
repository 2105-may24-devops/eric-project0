import os
import sys
import pickle
from . import paths

class TooManyDuplicates(Exception):
    def __init__(self, msg):
        self.msg = msg

class Payload:
    # this is a static variable which determines where all unpacked files be placed
    # changing this is only possible in the config.json file

    #need to change this as the pickled object will send to a server its own client dump_folder

    def __init__(self, root_folder : str, cwd=".", flatten : bool = False, files_to_read=list()):
        '''
        root_folder is where the contents of the data will be unpacked within the dump_folder static variable
        sender must set this variable, but if receiver has a folder of the same name, they too can change it.

        current_working_directory is where the search for all files/folders will begin

        flatten determines whether the files should retain thier directory structure when unpacked. If false it will, else not.

        __files_to_read is an optional arg to limit the number of files to read to the given names (paths must be absolute)

        self.payload is the data that has been traversed by get_files_wrapper i.e the data file/folder data

        '''
        self.root_folder = root_folder
        self.current_working_directory = cwd
        self.payload = []
        self.flatten = flatten
        self.__files_to_read = files_to_read
        # the format of payload is a list of dictionaries where {full_path: str, data: []byte, is_folder: bool}

    @property
    def windows(self):
        # if platform is windows, property returns true, else false
        return "win" in sys.platform

    def __recursive_files_and_folders(self, dir : str = None, data : list = None) -> list:
        if dir is None:
            # print(self.root_folder)
            # files_and_folders = os.scandir(self.root_folder)
            p = self.root_folder
            payload = list()
        else:
            # files_and_folders = os.scandir(dir)
            p = dir
            payload = data
        #print(list(files_and_folders)[0].is_dir(), type(files_and_folders), "yo")
        with os.scandir(p) as files_and_folders:
            for item in files_and_folders:

                if item.is_dir():
                    path, name = paths.path(item.path, self.windows)
                    folder = {"path": path, "name": name, "is_folder": True, "data": []}
                    payload.append(folder)
                    self.__recursive_files_and_folders(dir=folder["path"]+"/"+folder["name"], data=folder["data"])
                    continue
                
                # ignoring errors might result in loss of data...
                path, name = paths.path(item.path, self.windows)
                file_data = open(item.path, "r", encoding="utf8", errors="ignore")
                payload.append({"path": path, "name": name, "data": file_data.read(), "is_folder": False })
                file_data.close()
        return payload

    def __get_files_and_folders(self) -> list:
        files = list()
        for file_path in self.__files_to_read:
            try:
                path, name = paths.path(item.path, self.windows) #problem
                file = open(file_path, "r")
                files.append({"path": path, "name": name, "data": file.read(), "is_folder": False})
                file.close()
            except FileNotFoundError as e:
                print(e)
        return files

    def get_files(self) -> None:
        # calling function needs to do so in the try/except block
        if len(self.__files_to_read) == 0:
            self.payload = self.__recursive_files_and_folders()
        else:
            self.payload = self.__get_files_and_folders()

    def create_unpacking_dir(self, dump_folder):
        if "/" in self.root_folder:
            split = self.root_folder.split("/")
            self.root_folder = self.root_folder[len(split)]
        try:
            os.mkdir(dump_folder+"/"+self.root_folder)
            return None
        except FileExistsError:
            for i in range(1,1001):
                try:
                    os.mkdir(dump_folder+"/"+self.root_folder+"-"+str(i))
                    self.root_folder = self.root_folder+"-"+str(i)
                    return None
                except Exception as e:
                    pass
        raise TooManyDuplicates("Clean up your received folder or change instance variable root_folder. You have too many duplicates.")

    def unpack_files(self, payload, dump_folder : str, flatten = False) -> bool:
        #print(payload, "odaifjsofijdsfs")
        if len(payload) == 0:
            return False

        dump_in = f"{dump_folder}"
        #print(payload, "in here pls")
        for item in payload:
            path = item["path"].split("/")
            path[0] = self.root_folder
            item["path"] = '/'.join(path)
            
            if item["is_folder"]:
                if not flatten:
                    os.mkdir(dump_in + f"/{item['path']}/{item['name']}")
                success = self.unpack_files(item["data"], dump_folder, flatten)
                if not success:
                    return False
                continue
            #print(dump_in, "toot")
            try:
                path = item["name"] if flatten == True else f"{item['path']}/{item['name']}"
                #print(path)
                file = open(dump_in+"/"+path , "w", errors="ignore")
                file.write(item["data"])
                file.close()
            except Exception as e:
                print(e, "ex")
                return False
        return True

    def unpack_payload(self, dump_folder : str, flatten=False):
        self.create_unpacking_dir(dump_folder)
        #print("yes", dump_folder, self.root_folder)
        return self.unpack_files(self.payload, dump_folder, flatten)

    def pickle_dump(self) -> bytes:
        return pickle.dumps(self)
    
    @staticmethod
    def pickle_load(data : bytes): # returns Payload type
        return pickle.loads(data)



if __name__ == "__main__":
    f=Payload()
    f.get_files()
    #print(f.payload)
    # f=paths.remove_dot_slash("./fff/tt.txt")
    # print(f)