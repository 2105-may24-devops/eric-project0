# args:

# job: Job can only be five keywords; send, listen, ip, terminal or help. Must be final argument. Must be unnamed. This argument is required.

# -ip: ip address of the server to send to. required only if job=send.

# -port: default is 8000. Used when job is send or listen. Required if you want to send or listen to a port other than 8000.

# -to-send: required only if job=send. Can be a relative or absolute path. Can be many or or one argument. 
        If many, all arguments must be a path to a file. Argument must be formatted as -send='[path, path, path]'. 
        If one argument is enough, argument can be a file or a folder. Folders will be traversed recursively.
# -password: Only applicable if job is equal to send or listen. Default is 'nopassword'. 
        The client's password must match the server to which data is being sent, otherwise connection will be closed.
        Can be set in config.json or in the CLI.

# -cwd: cwd is applicable to terminal, send and listen. cwd is by default the location of this program.
        It can be set with either a relative or absolute path. Windows users MUST omit the "c:/" of a file.
        cwd will determine where the application's starting directory is. All relative paths will be based on it.
        by default cwd is the location of main.py. 
        A user can supply cwd through either a command line argument or pass it in config.json.

# -receive-folder: Folder where all received data is stored.
        This argument is only relevant when job=listen. When data is received, data is unpacked in cwd/received unless -receive-folder is set. This argument can be set in either the command line or config.json

# response code: 0=success, 1=bad password, 2=failed to unpack folders, 3=failed to initialize connection properly