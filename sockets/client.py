from .connection_initializer import Initializer
from progressbar import ProgressBar
from .encryption import encrypt
import socket
import logging



class Client:
    out = True

    # response codes
    success = b'0'
    bad_password = b'1'
    failed_on_unpacking = b'2'
    bad_initializer_msg = b'3'

    def __init__(self, address : tuple, data : bytes, password : str):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creates tcp socket which accepts IPv4 address
        self.socket.settimeout(2)

        self.socket.connect(address) # attempts to connect to given address
        # if this fails, it will raise a ConnectionRefusedError which must be caught
        # where the constructor is called

        self.socket.settimeout(None)
        self.payload : bytes = data
        self.password = password

    def send_initializer(self) -> tuple: # bytes and bool
        # if succesful the response to this will be a 64 byte key
        data = Initializer.make_init_message(len(self.payload), self.password)
        self.socket.sendall(data)
        resp = self.socket.recv(1)
        if resp != self.success:
            return resp, False
        recv = self.socket.recv(64)
        return recv, True

    def send_data(self, key) -> bytes:
        #print(len(self.payload), "sdfoisjdfsdojf")
        #self.socket.sendall(self.payload)
        bytes_sent = 0
        progress_bar = ProgressBar(max_value=len(self.payload))
        encrypted_data = encrypt(self.payload, key)
        while bytes_sent <= len(self.payload):
            if bytes_sent + 256 >= len(self.payload):
                self.socket.send(encrypted_data[bytes_sent:len(encrypted_data)])
                progress_bar.update(len(encrypted_data))
                break
            progress_bar.update(bytes_sent+256)
            self.socket.send(encrypted_data[bytes_sent:bytes_sent+256])
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
    def send_request(self):
        resp, resp_val = self.send_initializer()
        if not resp_val:
            self.socket.close()
            logging.getLogger("client").info(f"Request failed with a {resp.decode('utf8')}")
            return
        payload_response = self.send_data(resp)
        
        return self.parse_response(payload_response)






# if __name__ == "__main__":
#     send_data(('127.0.0.1', 8080), Initializer.make_init_message(5000, "nopassword"))