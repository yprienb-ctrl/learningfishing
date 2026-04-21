import base64
import re

def obfuscate_string(s: str) -> str:
    encoded = base64.b64encode(s.encode()).decode()
    return f"exec(base64.b64decode('{encoded}').decode())"

def obfuscate_file(input_file: str, output_file: str):
    with open(input_file, 'r') as f:
        content = f.read()
    content = re.sub(r'"([^"]*)"', lambda m: obfuscate_string(m.group(1)), content)
    content = re.sub(r"'([^']*)'", lambda m: obfuscate_string(m.group(1)), content)
    with open(output_file, 'w') as f:
        f.write(content)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    obfuscate_file(args.input, args.output)
