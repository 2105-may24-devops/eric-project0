import hashlib

# this class has four responsibilities:
# create the initial message which contains data length and password(used on client side)
# split the sent message on the server end
# hold the server password, and check whether the client's sent password matches the server's
class Initializer:

    #server's password
    server_password : str = None

    @staticmethod
    def make_init_message(data_length : int, password : str) -> bytes:
        # this method takes data_length and password(unhashed)
        # data_length is converted to a 32 bit integer. password is hashed with sha256(512 bits)
        # between them is a 24 bit seperator(":::")
        # (32+512+24)/8 = 71 bytes. This must always be true. 
        # If return value < 71, connection will timeout, if >71, msg will be cutoff 
        # function raises OverflowError if data_length > 4,294,967,295 (4.29 gb)
        length_32bits = data_length.to_bytes(4, "little")
        hashed_pass = hashlib.sha256(password.encode("utf-8")).hexdigest().encode("utf-8")
        return length_32bits + b':::' + hashed_pass

    @staticmethod
    def stringify_init_message(data : bytes) -> tuple: # (int, str)
        # parses init msg on server end, returns (str, int)
        b_array = data.partition(b':::')
        try:
            return ( int.from_bytes(b_array[0], "little"), b_array[2].decode("utf-8") )
        except:
            return (0, "")

    @staticmethod 
    def valid_password(client_password : str) -> bool:
        if Initializer.server_password is None:
            raise Exception("badbadbad!")
        return client_password == Initializer.server_password

    @staticmethod
    def set_server_password(password : str) -> None:
        # this function must run upon server startup INSIDE the ServerProcess's run method.
        # as the server process and this class run in seperate instances of the interpreter,
        # Handler.handler's Initializer class will have server_password = None if this rule is not followed.
        Initializer.server_password = hashlib.sha256(password.encode("utf-8")).hexdigest()