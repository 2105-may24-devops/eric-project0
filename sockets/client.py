import socket

def send_data(address, data) -> bool:
    #with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(address)
    s.sendall(data)
    b = s.recv(256)
    print(b)
    s.close()

if __name__ == "__main__":
    send_data(('127.0.0.1', 8080), b'123')