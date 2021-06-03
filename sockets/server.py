from multiprocessing import Process
import socketserver


# the only reasonable way to handle this shit is with a header message that tells you how many bytes arrive
# otherwise one socket will be forever waiting until EOF
class Handler(socketserver.StreamRequestHandler):
    timeout = 2
    def handle(self):
        print(self.rfile.read(3))
        f = self.wfile.write(b'123')
        print(f)

class ServerThread(Process):
    def __init__(self, address, *args, **kwargs):
        Process.__init__(self,*args, **kwargs)
        self.address = address

    def run(self):
        server = socketserver.TCPServer(self.address, Handler)
        while True:
            server.handle_request()

def run_server(address):
    server = ServerThread(address)
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
    run_server(("127.0.0.1", 8080))