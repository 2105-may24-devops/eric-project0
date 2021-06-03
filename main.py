# import blessed

# term = blessed.Terminal()

# from sockets import run_server

# run_server(("127.0.0.1", 8080), testing=False)

import sys
import json
from sockets.get_ip_address import get_own_ip




help_output = '''
# args:
# do: Do can only be five keywords; send, listen, ip, terminal or help. Must be final argument. Must be unnamed. This argument is required.
# -ip: ip address of the server to send to. required only if do=send.
# -port: default is 8000. Used when do is send or listen. Required if you want to send or listen to a port other than 8000.
# -send: required only if do=send. Can be a relative or absolute path. Can be many or or one argument. 
        If many, all arguments must be a path to a file. Argument must be formatted as -send='[path, path, path]'. 
        If one argument is enough, argument can be a file or a folder. Folders will be traversed recursively.
# -password: Only applicable if do is equal to send or listen. Default is 'nopassword'. 
        The client's password must match the server to which data is being sent, otherwise connection will be closed.
        Can be set in config.json or in the CLI.
# -cwd: cwd is applicable to terminal, send and listen. cwd is by default the location of this program.
        It can be set with either a relative or absolute path.
        cwd will determine where the application's starting directory is. All relative paths will be based on it.
        by default cwd is the location of main.py. 
        A user can supply cwd through either a command line argument or pass it in config.json.
# -receive-folder: Folder where all received data is stored.
        This argument is only relevant when do=listen. When data is received, data is unpacked in cwd/received unless -receive-folder is set
        This argument can be set in either the command line or config.json
# -max-bytes: Only applicable when do=listen. By default there is no max-bytes value. 
        If set, any amount sent above this maximum by a client will be rejected.
        Can be set in config.json or in the CLI.
'''

def main():
    args = sys.argv
    print(len(args), args)
    if len(args) == 0:
        print(args)
        print("Not enough arguments \n\n")

    if len(args) == 1 or args[len(args)-1] == "help" or args[len(args)-1] == "--help" or args[len(args)-1] == "-help":
        print(help_output)
        return None

    elif args[len(args)-1] == "ip":
        print("Your machine's ip address is", get_own_ip())

    elif args[len(args)-1] == "listen":
        pass

    



if __name__ == "__main__":
    main()