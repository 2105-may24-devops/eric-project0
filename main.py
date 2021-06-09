import os
import sys
import logging
from socket import timeout
from files.payload import Payload
from sockets.client import Client
from sockets.server import run_server
from sockets.get_ip_address import get_own_ip
from files.paths import get_cwd, convert_path

# if implementing encryption, do it like this
# 1- hashed password
# 2- receive back a key which has been encrypted with the plain text password
# 3- encrypt with the decrypted key


# all errors are intended to be caught by main
# whether they are printed to stdout and/or logged is up to the user

def create_logger(name, file):
    log_setup = logging.getLogger(name)
    formatter = logging.Formatter('%(asctime)s -- %(message)s', datefmt='%m/%d %I:%M %p')
    fileHandler = logging.FileHandler(file, mode='a')
    fileHandler.setFormatter(formatter)
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)
    log_setup.setLevel(logging.INFO)
    log_setup.addHandler(fileHandler)

def out(output, log, stdout=True):
    logging.getLogger(log).info(output)
    if stdout.lower() == "t":
        print(output)


create_logger("client", "logs/client.log")
create_logger("server", "logs/server.log")
create_logger("generic", "logs/general.log")

#os
windows = True if "win" in sys.platform else False

#argument defaults
PORT = 8080
PASSWORD = "nopassword"
CWD = get_cwd() #returns cwd in unix format
RECEIVE_FOLDER = "received"
STD_OUT = "t" # if false, data will not be printed to stdout
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
    
    # check if received-folder exists inside in given path and is a directory
    receive_folder = parsed_args.get("receive-folder", RECEIVE_FOLDER)
    if not any(filter(lambda x : x.name == receive_folder and x.is_dir(), os.scandir())):
        out(f"Couldn't find your intended receive-folder with name of '{receive_folder}'. Make sure it exists.", "server", parsed_args.get("out", STD_OUT))
        exit(1)
    # need to send receive into the backend somehow...
    try:
        run_server(("127.0.0.1", port), password, receive_folder, Payload)
    except:
        out("Failed to start server...", "server", parsed_args.get("out", STD_OUT))
            
def send(parsed_args):
    ip_address = parsed_args.get("ip", None)
    to_send = parsed_args.get("to-send", None)
    if ip_address is None or to_send is None:
        out(f"Need an argument for  {'ip' if ip_address is None else 'to-send'}", "client", parsed_args.get("out", STD_OUT))
        exit(1)
    port = parsed_args.get("port", PORT)
    password = parsed_args.get("password", PASSWORD)
    
    payload = Payload(to_send, flatten=False)

    try:
        payload.get_files()
    except FileNotFoundError:
        out(f"wasn't able to find folder {to_send}", "client", parsed_args.get("out", STD_OUT))
        exit(1)
    
    pp = payload.pickle_dump()
    
    try:
        client = Client((ip_address, port), pp, password)
    except timeout:
        out(f"Unable to connect to {ip_address}:{str(port)}", "client", parsed_args.get("out", STD_OUT))
        exit(1)

    try:
        res = client.send_request()
        if res:
            out(f"Succesfully sent folder '{to_send}' to {ip_address}", "client", parsed_args.get("out", STD_OUT))
        else:
            out(f"Failed to send {to_send}, check logs for details", "client", parsed_args.get("out", STD_OUT))
    except Exception as e:
        print(e)
        out(f"Failed to send complete request to {ip_address}:{str(port)}", "client", parsed_args.get("out", STD_OUT))

def main():
    args = sys.argv
    if len(args) == 0:
        out("Need at least one argument", "generic")

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

    else:
        out("Unknown final argument", "generic", parsed_args.get("out", STD_OUT))
    



if __name__ == "__main__":
    main()