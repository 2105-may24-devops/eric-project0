from .connection_initializer import Initializer
from multiprocessing import Process
import socketserver

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

    PayloadClass = None # all this class must implement is a static method named pickle_load and an instance variable named payload

    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)
        if self.PayloadClass is None:
            raise Exception("Payload Class must be set")

    def handle(self):
        msg_length, valid = self.middleware()
        if not valid:
            return
        print("success", msg_length)
        # receive payload and unpack here
        self.wfile.write(Handler.success)

        payload_bytes = self.rfile.read(msg_length)
        payload = self.PayloadClass.pickle_load(payload_bytes)
        print(payload.root_folder)

    def middleware(self) -> bool:
        # parses initializer message from client
        # checks password, if password is valid, returns msg_length and True
        # if not valid, returns 0, False
        b_array = self.rfile.read(71)
        data_length, client_password = Initializer.stringify_init_message(b_array)
        print(data_length, client_password, Initializer.valid_password(client_password))
        if client_password == "":
            self.wfile.write(Handler.bad_initializer_msg)
            return 0, False
        if not Initializer.valid_password(client_password):
            self.wfile.write(Handler.bad_password)
            return 0, False
        return data_length, True

class ServerThread(Process):

    def __init__(self, address, server_password, PayloadClass, *args, **kwargs):
        Process.__init__(self,*args, **kwargs)
        self.address = address
        self.server_password = server_password
        self.PayloadClass = PayloadClass

    def run(self):
        Handler.PayloadClass = self.PayloadClass
        server = socketserver.TCPServer(self.address, Handler)
        Initializer.set_server_password(self.server_password)

        while True:
            server.handle_request()

def run_server(address, server_password, PayloadClass):
    server = ServerThread("*", server_password, PayloadClass)
    server.start()
    print(f"Server listing on {address[0]}:{address[1]}")
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