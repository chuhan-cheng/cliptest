import socket
import subprocess
import time

DEVICE_A_IP = '192.168.225.129' # 請修改為 A 的 IP
PORT = 65432
FIFO_PATH = "/tmp/clipboard_fifo"
def setup_wayland_lazy():
    if os.path.exists(FIFO_PATH):
        os.remove(FIFO_PATH)
    os.mkfifo(FIFO_PATH)

    print("🚀 Wayland 延遲渲染服務啟動...")

    # --- 修正處 1：不要在 Python 裡 open，讓 shell 處理重導向 ---
    # 使用 shell=True 讓 wl-copy < /tmp/clipboard_fifo 在背景等待
    # 這樣 Python 就不會卡在 open()
    cmd = f"wl-copy --type text/plain --foreground --paste-once < {FIFO_PATH}"
    copy_proc = subprocess.Popen(cmd, shell=True)

    print("📢 剪貼簿已就位，等待『貼上』觸發網路連線...")

    try:
        # --- 修正處 2：這行會卡住，直到你按「貼上」 ---
        # 當你按貼上，wl-copy 開始讀，這行 open("w") 才會解除阻塞並繼續執行
        with open(FIFO_PATH, "w") as fifo:
            print("\n[偵測到貼上動作！] 正在向 A 裝置索取資料...")

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(5)
                s.connect((DEVICE_A_IP, PORT))
                data = s.recv(4096).decode()
                fifo.write(data)
                fifo.flush() # 確保資料送出
                print("✅ 資料傳輸完成。")

    except Exception as e:
        print(f"❌ 錯誤: {e}")
    finally:
        copy_proc.terminate()
        if os.path.exists(FIFO_PATH):
            os.remove(FIFO_PATH)

if __name__ == "__main__":
    setup_wayland_lazy()
