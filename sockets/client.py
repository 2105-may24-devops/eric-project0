from .connection_initializer import Initializer
from progressbar import ProgressBar
import socket

class Client:
    # response codes
    success = b'0'
    bad_password = b'1'
    failed_on_unpacking = b'2'
    bad_initializer_msg = b'3'

    def __init__(self, address : tuple, data : bytes):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creates tcp socket which accepts IPv4 address
        self.socket.settimeout(2)
        try:
            self.socket.connect(address) # attempts to connect to given address
            # if this fails, it will raise a ConnectionRefusedError which must be caught
            # where the constructor is called
        except ConnectionRefusedError:
            print(f"Couldn't connect to {self.address[0]}:{self.address[1]}")
            exit(1)
        self.socket.settimeout(None)
        self.payload : bytes = data

    def send_initializer(self, password : str) -> bytes:
        data = Initializer.make_init_message(len(self.payload), password)
        self.socket.sendall(data)
        recv = self.socket.recv(1)
        return recv

    def send_data(self) -> bytes:
        #print(len(self.payload), "sdfoisjdfsdojf")
        #self.socket.sendall(self.payload)
        bytes_sent = 0
        progress_bar = ProgressBar(max_value=len(self.payload))
        while bytes_sent <= len(self.payload):
            if bytes_sent + 256 >= len(self.payload):
                self.socket.send(self.payload[bytes_sent:len(self.payload)])
                progress_bar.update(len(self.payload))
                break
            progress_bar.update(bytes_sent+256)
            self.socket.send(self.payload[bytes_sent:bytes_sent+256])
            bytes_sent+=256
        progress_bar.finish()
        recv = self.socket.recv(1)
        return recv

    # if it returns True, the data was sent succesfully. Otherwise, something went wrong.
    def parse_response(self, response):
        if response == self.success:
            print("success")
            return True
        elif response == self.bad_password:
            print("bad password")
        elif response == self.failed_on_unpacking:
            print("server couldn't unpack you paylaod")
        elif response == self.bad_initializer_msg:
            print("you sent the server a bad initializer message")
        
        return False

    # this method wraps the above two, sending the whole request
    def send_request(self, password : str):
        initial_response = self.send_initializer(password)
        if not self.parse_response(initial_response):
            self.socket.close()
            return
        payload_response = self.send_data()
        
        self.parse_response(payload_response)
        return






# if __name__ == "__main__":
#     send_data(('127.0.0.1', 8080), Initializer.make_init_message(5000, "nopassword"))