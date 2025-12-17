import socket
import subprocess

def get_actual_clipboard():
    # 這裡模擬讀取 A 的實際內容，可以是檔案、圖片或文字
    try:
        # 假設 A 也是 Wayland，讀取 A 的剪貼簿
        return subprocess.check_output(['wl-paste', '--no-newline'])
    except:
        return b"Hello from Device A! (Actual Data)"

def start_provider(port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('0.0.0.0', port))
        s.listen(5)
        print(f"📡 裝置 A 已啟動，等待貼上請求於 port {port}...")
        
        while True:
            conn, addr = s.accept()
            with conn:
                print(f"✨ 偵測到 B 裝置的『貼上』請求 (來源: {addr})")
                data = get_actual_clipboard()
                conn.sendall(data)
                print("✅ 數據傳送完成。")

if __name__ == "__main__":
    start_provider()
