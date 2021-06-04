# import blessed

# term = blessed.Terminal()

# from sockets import run_server

# run_server(("127.0.0.1", 8080), testing=False)

import sys
import json
from sockets.get_ip_address import get_own_ip
from sockets.server import run_server




help_output = '''
# args:
# job: Job can only be five keywords; send, listen, ip, terminal or help. Must be final argument. Must be unnamed. This argument is required.
# -ip: ip address of the server to send to. required only if job=send.
# -port: default is 8000. Used when job is send or listen. Required if you want to send or listen to a port other than 8000.
# -send: required only if job=send. Can be a relative or absolute path. Can be many or or one argument. 
        If many, all arguments must be a path to a file. Argument must be formatted as -send='[path, path, path]'. 
        If one argument is enough, argument can be a file or a folder. Folders will be traversed recursively.
# -password: Only applicable if job is equal to send or listen. Default is 'nopassword'. 
        The client's password must match the server to which data is being sent, otherwise connection will be closed.
        Can be set in config.json or in the CLI.
# -cwd: cwd is applicable to terminal, send and listen. cwd is by default the location of this program.
        It can be set with either a relative or absolute path.
        cwd will determine where the application's starting directory is. All relative paths will be based on it.
        by default cwd is the location of main.py. 
        A user can supply cwd through either a command line argument or pass it in config.json.
# -receive-folder: Folder where all received data is stored.
        This argument is only relevant when job=listen. When data is received, data is unpacked in cwd/received unless -receive-folder is set
        This argument can be set in either the command line or config.json
# -max-bytes: Only applicable when job=listen. By default 4,294,967,296 is the max bytes(4.29 GB). 
        Any amount sent above this maximum by a client will be rejected. Cannot only be less than the default, cannot be increased.
        Can be set in config.json or in the CLI.
'''

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


def main():
    args = sys.argv
    print(len(args), args)
    if len(args) == 0:
        print(args)
        print("Not enough arguments \n\n")

    final_arg = get_final_arg()
    if len(args) == 1 or final_arg is None or final_arg == "help":
        print(help_output)
        return None

    parsed_args = parse_args()
    print(parsed_args)
    
    if final_arg == "ip":
        print("Your machine's ip address is", get_own_ip())
        return

    elif final_arg == "listen":
        run_server(("127.0.0.1", 8080), "mypassword")

    



if __name__ == "__main__":
    main()