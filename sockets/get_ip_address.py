import socket 

def get_own_ip() -> str:
    info = socket.gethostbyname_ex(socket.gethostname())
    return info[len(info)-1][0]
