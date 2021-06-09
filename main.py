import os
import sys
from files.payload import Payload
from sockets.client import Client
from sockets.server import run_server
from sockets.get_ip_address import get_own_ip
from files.paths import get_cwd, convert_path

# if implementing encryption, do it like this
# 1- hashed password
# 2- receive back a key which has been encrypted with the plain text password
# 3- encrypt with the decrypted key

#os
windows = True if "win" in sys.platform else False

#argument defaults
PORT = 8080
PASSWORD = "nopassword"
CWD = get_cwd() #returns cwd in unix format
RECEIVE_FOLDER = "received"
MAX_BYTES = 1 << 32 # not integrated...


def get_final_arg():
    options = {"help", "ip", "listen", "send", "terminal"}
    if sys.argv[len(sys.argv)-1] in options:
        return sys.argv[len(sys.argv)-1]
    return None

def parse_args():
    args = sys.argv
    return_value = dict()

    for arg in args:
        if "=" in arg:
            split = arg.split("=")
            return_value[split[0]] = split[1]

    return return_value

def listen(parsed_args):
    port = parsed_args.get("port", PORT)
    password = parsed_args.get("password", PASSWORD)
    if parsed_args.get("cwd", None) is not None:
        try:
            print(convert_path(parsed_args.get("cwd")), parsed_args.get("cwd"))
            os.chdir(parsed_args.get("cwd"))
        except Exception as e:
            print("Unable to change dir to given cwd argument.", e)
            exit(1)
    
    # check if received-folder exists inside in given path and is a directory
    receive_folder = parsed_args.get("receive-folder", RECEIVE_FOLDER)
    if not any(filter(lambda x : x.name == receive_folder and x.is_dir(), os.scandir())):
        print("Couldn't find your intended received-folder. Make sure it exists.")
        exit(1)
    # need to send receive into the backend somehow...
    run_server(("127.0.0.1", port), password, receive_folder, Payload)
            
def send(parsed_args):
    ip_address = parsed_args.get("ip", None)
    to_send = parsed_args.get("to-send", None)
    if ip_address is None or to_send is None:
        print(f"Need an argument for  {'ip' if ip_address is None else 'to-send'}")
        exit(1)
    port = parsed_args.get("port", PORT)
    password = parsed_args.get("password", PASSWORD)
    if parsed_args.get("cwd", None):
        try:
            os.chdir(parsed_args.get("cwd"))
        except Exception as e:
            print("Given argument for cwd could not be found", e) #use files.paths library
            exit(1)
    
    payload = Payload(to_send, flatten=False)
    payload.get_files()
    pp = payload.pickle_dump()
    client = Client((ip_address, port), pp)
    client.send_request(password)

def main():
    args = sys.argv
    if len(args) == 0:
        print("Not enough arguments \n\n")

    final_arg = get_final_arg()
    if len(args) == 1 or final_arg is None or final_arg == "help":
        file = open("README.md", "r")
        print(file.read())
        file.close()
        return None

    parsed_args = parse_args()
    
    if final_arg == "ip":
        print("Your machine's ip address is", get_own_ip())
        return

    elif final_arg == "listen":
        listen(parsed_args)

    elif final_arg == "send":
        send(parsed_args)

    



if __name__ == "__main__":
    main()