import secrets
from arc4 import ARC4

def encrypt(data : bytes, key : bytes) -> bytes:
    cipher = ARC4(key)
    return cipher.encrypt(data)

def decrypt(data : bytes, key : bytes) -> bytes:
    cipher = ARC4(key)
    return cipher.encrypt(data)

def generate_key(encrypt_with) -> bytes:
    return secrets.token_bytes(64)