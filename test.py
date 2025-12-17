# device_a_provider.py
import socket
import subprocess

def get_local_clipboard():
    # 使用 xclip 作為範例 (Linux)，Windows 可改用 pywin32
    try:
        return subprocess.check_output(['xclip', '-selection', 'clipboard', '-o'])
    except:
        return b"Error reading clipboard"

def start_provider(host='0.0.0.0', port=65432):
    data = get_local_clipboard()
    print(data)

if __name__ == "__main__":
    start_provider()
