import base64
import os
import sys
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes

def derive_key(password: str, salt: bytes, length: int = 32) -> bytes:
    return PBKDF2(password, salt, dkLen=length, count=100_000)

def encrypt(plain_text: str, password: str) -> str:
    salt = get_random_bytes(16)
    key = derive_key(password, salt)
    cipher = AES.new(key, AES.MODE_GCM)
    nonce = cipher.nonce
    ct = cipher.encrypt(plain_text.encode())
    return base64.b64encode(salt + nonce + ct).decode()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python encrypt_webhook.py <WEBWALK_URL> <PASSWORD>")
        sys.exit(1)
    url = sys.argv[1]
    pwd = sys.argv[2]
    encrypted = encrypt(url, pwd)
    print(encrypted)
