import socketserver
import logging
from .encryption import generate_key, decrypt
from .connection_initializer import Initializer
from .get_ip_address import get_own_ip
from multiprocessing import Process


def server_log(out):
    print(out)
    logging.getLogger("server").info(out)

# server_password = "nopassword"
# the only reasonable way to handle this shit is with a header message that tells you how many bytes arrive
# otherwise one socket will be forever waiting until EOF
class Handler(socketserver.StreamRequestHandler):
    timeout = 2 # two second timeout

    # response codes
    success = b'0'
    bad_password = b'1'
    failed_on_unpacking = b'2'
    bad_initializer_msg = b'3'

    receive_folder = None
    PayloadClass = None # all this class must implement is a static method named pickle_load and an instance variable named payload

    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)
        if self.PayloadClass is None or self.receive_folder is None:
            raise Exception("Payload Class must be set")

    def handle(self):
        msg_length, if_error, valid = self.middleware()
        if not valid:
            self.wfile.write(if_error)
            server_log(f"Connection from {self.client_address[0]} closed with error code {if_error.decode('utf8')}")
            return
        
        self.wfile.write(self.success)
        key = generate_key(Initializer.server_password)
        self.wfile.write(key)
        payload_bytes = self.rfile.read(msg_length)
        payload = self.PayloadClass.pickle_load(decrypt(payload_bytes, key))
        if not payload.unpack_payload(self.receive_folder):
            self.wfile.write(self.failed_on_unpacking)
            server_log(f"Failed to unpack received data from {self.client_address[0]}")
            return
        server_log(f"Succesfully received and unpacked {payload.root_folder} from {self.client_address[0]}")
        self.wfile.write(Handler.success)
            

    def middleware(self) -> tuple: # response
        # parses initializer message from client
        # checks password, if password is valid, returns msg_length and True
        # if not valid, returns 0, False
        b_array = self.rfile.read(71)
        data_length, client_password = Initializer.stringify_init_message(b_array)

        if client_password == "":
            self.wfile.write(Handler.bad_initializer_msg)
            return 0, self.bad_initializer_msg, False
        
        if not Initializer.valid_password(client_password):
            self.wfile.write(Handler.bad_password)
            return 0, self.bad_password, False
        return data_length, 0,  True

class ServerThread(Process):

    def __init__(self, address, server_password, receive_folder, PayloadClass, *args, **kwargs):
        Process.__init__(self, *args, **kwargs)
        self.address = address
        self.server_password = server_password
        self.receive_folder = receive_folder
        self.PayloadClass = PayloadClass

    def run(self):
        Handler.PayloadClass = self.PayloadClass
        Handler.receive_folder = self.receive_folder
        server = socketserver.TCPServer((get_own_ip(), 8080), Handler)
        Initializer.set_server_password(self.server_password)

        while True:
            server.handle_request()

def run_server(address, server_password, receive_folder, PayloadClass):
    server = ServerThread(address, server_password, receive_folder, PayloadClass)
    server.start()
    print(f"Server listing on {get_own_ip()}:{address[1]}")
    print("Enter 'q' to quit.")
    while True:
        try:
            q = input()
            if q == "q":
                server.terminate()
                break
        except KeyboardInterrupt:
            q = "q"

if __name__  == "__main__":
    run_server(("127.0.0.1", 8080), "mypassword")