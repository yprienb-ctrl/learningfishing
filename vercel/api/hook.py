import os
import base64
import json
import requests
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from flask import Flask, request, jsonify

app = Flask(__name__)

def derive_key(password: str, salt: bytes, length: int = 32) -> bytes:
    return PBKDF2(password, salt, dkLen=length, count=100_000)

def decrypt(encrypted_blob: str, password: str) -> str:
    data = base64.b64decode(encrypted_blob)
    salt = data[:16]
    nonce = data[16:28]
    tag = data[-16:]
    ct = data[28:-16]
    key = derive_key(password, salt)
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    try:
        plaintext = cipher.decrypt_and_verify(ct, tag)
        return plaintext.decode()
    except Exception as e:
        raise ValueError("Decryption failed – invalid key or corrupted data") from e

WEBHOOK_BLOB = os.getenv("WEBHOOK_BLOB")
WEBHOOK_KEY  = os.getenv("WEBHOOK_KEY")

if not (WEBHOOK_BLOB and WEBHOOK_KEY):
    raise RuntimeError("WEBHOOK_BLOB and WEBHOOK_KEY must be set in env")

def send_to_discord(payload: dict):
    webhook_url = decrypt(WEBHOOK_BLOB, WEBHOOK_KEY)
    requests.post(webhook_url, json=payload)

@app.route('/api/hook', methods=['POST'])
def endpoint():
    if request.method == "POST":
        body = request.get_json()
        if not body or "data" not in body:
            return jsonify({"error": "Invalid payload"}), 400
        try:
            webhook_url = decrypt(WEBHOOK_BLOB, WEBHOOK_KEY)
            requests.post(webhook_url, json=body)
        except Exception as exc:
            return jsonify({"error": str(exc)}), 500
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
