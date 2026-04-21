import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

def generate_key() -> bytes:
    return get_random_bytes(32)

def encrypt(data: str, key: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(data.encode())
    return cipher.nonce + ciphertext + tag

def decrypt(ciphertext: bytes, key: bytes) -> str:
    nonce = ciphertext[:16]
    tag = ciphertext[-16:]
    data = ciphertext[16:-16]
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    return cipher.decrypt_and_verify(data, tag).decode()

def key_from_env() -> bytes:
    key_b64 = os.getenv("CRYPTO_KEY")
    if not key_b64:
        raise ValueError("CRYPTO_KEY not set")
    return base64.b64decode(key_b64)
